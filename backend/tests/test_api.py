import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.db import connect, transaction
from app.identity import Identity, get_current_identity
from app.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.getenv("SUPPORT_TEST_DATABASE") != "true":
            raise unittest.SkipTest("requires explicit SUPPORT_TEST_DATABASE=true")
        with transaction() as db:
            cls.org_a = db.execute("INSERT INTO organizations (name,slug) VALUES (%s,%s) RETURNING id", ("Backend Test A", "backend-test-a")).fetchone()["id"]
            cls.org_b = db.execute("INSERT INTO organizations (name,slug) VALUES (%s,%s) RETURNING id", ("Backend Test B", "backend-test-b")).fetchone()["id"]
            cls.user_a = db.execute("INSERT INTO users (name,email) VALUES (%s,%s) RETURNING id", ("Backend User A", "backend.a@example.invalid")).fetchone()["id"]
            cls.user_b = db.execute("INSERT INTO users (name,email) VALUES (%s,%s) RETURNING id", ("Backend User B", "backend.b@example.invalid")).fetchone()["id"]
            cls.product_a = db.execute("INSERT INTO products (name,slug) VALUES (%s,%s) RETURNING id", ("Backend Product A", "backend-product-a")).fetchone()["id"]
            cls.product_b = db.execute("INSERT INTO products (name,slug) VALUES (%s,%s) RETURNING id", ("Backend Product B", "backend-product-b")).fetchone()["id"]
            cls.product_inactive = db.execute("INSERT INTO products (name,slug,status) VALUES (%s,%s,'inactive') RETURNING id", ("Backend Inactive", "backend-inactive")).fetchone()["id"]
            db.execute("INSERT INTO organization_members (organization_id,user_id) VALUES (%s,%s),(%s,%s)", (cls.org_a, cls.user_a, cls.org_b, cls.user_b))
            db.execute("INSERT INTO organization_products (organization_id,product_id) VALUES (%s,%s),(%s,%s),(%s,%s)", (cls.org_a, cls.product_a, cls.org_a, cls.product_inactive, cls.org_b, cls.product_b))
            cls.ticket_a = db.execute("INSERT INTO tickets (reference_code,organization_id,product_id,created_by_user_id,title,priority) VALUES (%s,%s,%s,%s,%s,'p3') RETURNING id", ("BACKEND-TEST-A", cls.org_a, cls.product_a, cls.user_a, "Ticket A")).fetchone()["id"]
            cls.ticket_b = db.execute("INSERT INTO tickets (reference_code,organization_id,product_id,created_by_user_id,title,priority) VALUES (%s,%s,%s,%s,%s,'p3') RETURNING id", ("BACKEND-TEST-B", cls.org_b, cls.product_b, cls.user_b, "Ticket B")).fetchone()["id"]
            db.execute("INSERT INTO ticket_messages (ticket_id,author_user_id,body) VALUES (%s,%s,%s)", (cls.ticket_a, cls.user_a, "Initial A"))
            db.execute("INSERT INTO ticket_events (ticket_id,actor_user_id,event_type,metadata) VALUES (%s,%s,'created','{}')", (cls.ticket_a, cls.user_a))
        app.dependency_overrides[get_current_identity] = lambda: Identity(cls.org_a, cls.user_a)
        cls.client = TestClient(app, raise_server_exceptions=False)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        with transaction() as db:
            ticket_ids = [row["id"] for row in db.execute("SELECT id FROM tickets WHERE organization_id IN (%s,%s)", (cls.org_a, cls.org_b)).fetchall()]
            if ticket_ids:
                db.execute("DELETE FROM ticket_attachments WHERE message_id IN (SELECT id FROM ticket_messages WHERE ticket_id = ANY(%s))", (ticket_ids,))
                db.execute("DELETE FROM ticket_events WHERE ticket_id = ANY(%s)", (ticket_ids,))
                db.execute("DELETE FROM ticket_messages WHERE ticket_id = ANY(%s)", (ticket_ids,))
                db.execute("DELETE FROM tickets WHERE id = ANY(%s)", (ticket_ids,))
            db.execute("DELETE FROM organization_products WHERE organization_id IN (%s,%s)", (cls.org_a, cls.org_b))
            db.execute("DELETE FROM organization_members WHERE organization_id IN (%s,%s)", (cls.org_a, cls.org_b))
            db.execute("DELETE FROM products WHERE id = ANY(%s)", ([cls.product_a, cls.product_b, cls.product_inactive],))
            db.execute("DELETE FROM users WHERE id = ANY(%s)", ([cls.user_a, cls.user_b],))
            db.execute("DELETE FROM organizations WHERE id IN (%s,%s)", (cls.org_a, cls.org_b))

    def test_01_health(self):
        self.assertEqual(self.client.get("/health").json(), {"status": "ok", "database": "ok"})

    def test_02_health_database_failure(self):
        with patch("app.main.connect", side_effect=RuntimeError("unavailable")):
            response = self.client.get("/health")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"detail": "Service unavailable"})

    def test_03_products_are_scoped_and_active(self):
        response = self.client.get("/api/products")
        self.assertEqual([item["id"] for item in response.json()], [self.product_a])

    def test_04_tickets_are_scoped(self):
        ids = [item["id"] for item in self.client.get("/api/tickets").json()]
        self.assertIn(self.ticket_a, ids)
        self.assertNotIn(self.ticket_b, ids)

    def test_05_cross_tenant_and_missing_ticket_are_404(self):
        self.assertEqual(self.client.get(f"/api/tickets/{self.ticket_b}").status_code, 404)
        self.assertEqual(self.client.get("/api/tickets/999999999").status_code, 404)

    def test_06_create_ticket_and_server_reference(self):
        response = self.client.post("/api/tickets", json={"product_id": self.product_a, "title": "Created", "priority": "p2", "message": "Initial"})
        self.assertEqual(response.status_code, 201, response.text)
        self.assertRegex(response.json()["reference_code"], r"^KDH-\d{4}-\d{6}$")
        ticket_id = response.json()["id"]
        self.assertEqual(len(self.client.get(f"/api/tickets/{ticket_id}/messages").json()), 1)
        self.assertEqual(self.client.get(f"/api/tickets/{ticket_id}/events").json()[0]["event_type"], "created")

    def test_07_product_rules(self):
        base = {"title": "Invalid", "priority": "p2", "message": "Initial"}
        self.assertEqual(self.client.post("/api/tickets", json={**base, "product_id": self.product_b}).status_code, 400)
        self.assertEqual(self.client.post("/api/tickets", json={**base, "product_id": self.product_inactive}).status_code, 400)

    def test_08_payload_validation(self):
        base = {"product_id": self.product_a, "title": "Valid", "priority": "p2", "message": "Initial"}
        for change in ({"priority": "p9"}, {"title": "   "}, {"message": "   "}):
            self.assertEqual(self.client.post("/api/tickets", json={**base, **change}).status_code, 422)

    def test_09_transaction_rolls_back_orphan_ticket(self):
        with connect() as db:
            before = db.execute("SELECT count(*) AS value FROM tickets WHERE organization_id=%s", (self.org_a,)).fetchone()["value"]
        with self.assertRaises(RuntimeError):
            with transaction() as db:
                db.execute("INSERT INTO tickets (reference_code,organization_id,product_id,created_by_user_id,title,priority) VALUES (%s,%s,%s,%s,%s,'p3')", ("ATOMIC-ROLLBACK", self.org_a, self.product_a, self.user_a, "Atomic"))
                raise RuntimeError("message failure")
        with connect() as db:
            after = db.execute("SELECT count(*) AS value FROM tickets WHERE organization_id=%s", (self.org_a,)).fetchone()["value"]
        self.assertEqual(before, after)

    def test_10_messages_and_events_are_scoped(self):
        response = self.client.post(f"/api/tickets/{self.ticket_a}/messages", json={"body": "Reply"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.post(f"/api/tickets/{self.ticket_a}/messages", json={"body": " "}).status_code, 422)
        self.assertEqual(self.client.post(f"/api/tickets/{self.ticket_b}/messages", json={"body": "No"}).status_code, 404)
        self.assertEqual(self.client.get(f"/api/tickets/{self.ticket_b}/events").status_code, 404)
        self.assertTrue(self.client.get(f"/api/tickets/{self.ticket_a}/events").json())
