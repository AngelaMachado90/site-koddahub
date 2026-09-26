import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "database" / "migrations"


class DatabaseMigrationStaticTests(unittest.TestCase):
    """Checks repository invariants; does not validate PostgreSQL syntax."""

    @classmethod
    def setUpClass(cls):
        cls.paths = sorted(MIGRATIONS.glob("*.sql"))
        cls.contents = {path.name: path.read_text(encoding="utf-8") for path in cls.paths}
        cls.combined = "\n".join(cls.contents.values())

    def test_migrations_have_expected_contiguous_sequence(self):
        expected = [
            "001_create_organizations.sql",
            "002_create_users.sql",
            "003_create_user_identities.sql",
            "004_create_organization_members.sql",
            "005_create_products.sql",
            "006_create_organization_products.sql",
            "007_create_tickets.sql",
            "008_create_ticket_messages.sql",
            "009_create_ticket_attachments.sql",
            "010_create_ticket_events.sql",
            "011_create_support_indexes.sql",
        ]
        self.assertEqual([path.name for path in self.paths], expected)
        numbers = [path.name.split("_", 1)[0] for path in self.paths]
        self.assertEqual(len(numbers), len(set(numbers)))

    def test_every_migration_is_transactional_and_has_final_newline(self):
        for name, sql in self.contents.items():
            with self.subTest(migration=name):
                executable = re.sub(r"(?m)^--.*$", "", sql).strip()
                self.assertTrue(executable.startswith("BEGIN;"))
                self.assertTrue(executable.endswith("COMMIT;"))
                self.assertEqual(executable.count("BEGIN;"), 1)
                self.assertEqual(executable.count("COMMIT;"), 1)
                self.assertTrue(sql.endswith("\n"))

    def test_expected_tables_are_created_once(self):
        expected = {
            "organizations",
            "users",
            "user_identities",
            "organization_members",
            "products",
            "organization_products",
            "tickets",
            "ticket_messages",
            "ticket_attachments",
            "ticket_events",
        }
        created = re.findall(r"(?im)^CREATE TABLE ([a-z_]+) ", self.combined)
        self.assertEqual(set(created), expected)
        self.assertEqual(len(created), len(set(created)))

    def test_primary_relationships_and_product_scope_are_explicit(self):
        required_fragments = (
            "REFERENCES users (id) ON DELETE RESTRICT",
            "REFERENCES organizations (id)",
            "REFERENCES products (id) ON DELETE RESTRICT",
            "REFERENCES organization_products (organization_id, product_id)",
            "REFERENCES tickets (id) ON DELETE RESTRICT",
            "REFERENCES ticket_messages (id) ON DELETE RESTRICT",
            "UNIQUE (organization_id, user_id)",
            "UNIQUE (organization_id, product_id)",
            "UNIQUE (provider, provider_subject)",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.combined)

    def test_domains_and_content_constraints_exist(self):
        for fragment in (
            "users_email_canonical",
            "tickets_status_valid",
            "tickets_priority_valid",
            "ticket_messages_body_not_blank",
            "ticket_attachments_size_nonnegative",
            "ticket_events_metadata_object",
        ):
            with self.subTest(constraint=fragment):
                self.assertIn(fragment, self.combined)

    def test_support_indexes_cover_expected_access_paths(self):
        indexes = self.contents["011_create_support_indexes.sql"]
        for columns in (
            "(user_id, status)",
            "(product_id, status)",
            "(organization_id, updated_at DESC)",
            "(organization_id, status, updated_at DESC)",
            "(assigned_to_user_id, status, updated_at DESC)",
            "(ticket_id, created_at, id)",
        ):
            with self.subTest(columns=columns):
                self.assertIn(columns, indexes)

    def test_migrations_avoid_destructive_statements_and_embedded_credentials(self):
        forbidden_patterns = (
            r"(?i)DROP\s+(?:DATABASE|TABLE)",
            r"(?i)TRUNCATE\s+TABLE",
            r"(?i)CREATE\s+(?:DATABASE|ROLE|USER)",
            r"(?i)(?:password|access_token|refresh_token|client_secret)\s*=",
            r"(?i)postgres(?:ql)?://[^\s]+:[^\s]+@",
        )
        for name, sql in self.contents.items():
            for pattern in forbidden_patterns:
                with self.subTest(migration=name, pattern=pattern):
                    self.assertIsNone(re.search(pattern, sql))

    def test_migrations_have_no_trailing_whitespace(self):
        for name, sql in self.contents.items():
            with self.subTest(migration=name):
                self.assertFalse(any(line != line.rstrip() for line in sql.splitlines()))


if __name__ == "__main__":
    unittest.main()
