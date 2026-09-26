import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_build_module():
    build_path = ROOT / "scripts/build.py"
    spec = importlib.util.spec_from_file_location("site_build", build_path)
    module = importlib.util.module_from_spec(spec)
    old_path = list(sys.path)
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = old_path
    return module


class PortalDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.dist = Path(cls.temporary.name) / "dist"
        cls.build_module = load_build_module()
        cls.build_module.DIST = cls.dist
        with patch.dict(os.environ, {"ASSET_VERSION": "portal-demo-test"}):
            cls.build_module.build()
        cls.routes = {
            "login": cls.dist / "portal/demo/index.html",
            "dashboard": cls.dist / "portal/demo/dashboard/index.html",
            "tickets": cls.dist / "portal/demo/chamados/index.html",
            "detail": cls.dist / "portal/demo/chamados/detalhe/index.html",
            "new": cls.dist / "portal/demo/chamados/novo/index.html",
        }

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_build_generates_every_direct_demo_route(self):
        for route, path in self.routes.items():
            with self.subTest(route=route):
                self.assertTrue(path.is_file(), path)
                self.assertNotIn("{{", path.read_text(encoding="utf-8"))

    def test_internal_pages_expose_demo_notice_and_navigation(self):
        for route in ("dashboard", "tickets", "detail", "new"):
            page = self.routes[route].read_text(encoding="utf-8")
            with self.subTest(route=route):
                self.assertIn("Ambiente HML sem autenticação produtiva", page)
                self.assertIn("dados são persistidos no PostgreSQL HML", page)
                self.assertIn('href="/portal/demo/dashboard/"', page)
                self.assertIn('href="/portal/demo/chamados/"', page)
                self.assertIn('href="/portal/demo/chamados/novo/"', page)
                self.assertIn('href="/portal/demo/"', page)

    def test_internal_pages_identify_hml_and_login_identifies_demo_entry(self):
        self.assertIn("Ambiente de demonstração", self.routes["login"].read_text(encoding="utf-8"))
        for route in ("dashboard", "tickets", "detail", "new"):
            page = self.routes[route].read_text(encoding="utf-8")
            self.assertIn("Ambiente HML sem autenticação produtiva", page)

    def test_original_portal_login_continues_to_be_generated(self):
        self.assertTrue((self.dist / "portal/login/index.html").is_file())

    def test_login_has_explicit_demo_access_without_credentials(self):
        page = self.routes["login"].read_text(encoding="utf-8")
        self.assertIn("Entrar na demonstração", page)
        self.assertIn("Marina Costa", page)
        self.assertIn("Empresa Demonstração", page)
        self.assertNotIn('type="password"', page)

    def test_mock_data_contains_required_tickets_and_products(self):
        fixture = (self.dist / "assets/js/portal-demo-data.js").read_text(encoding="utf-8")
        for expected in (
            "KDH-2026-000042",
            "KDH-2026-000041",
            "KDH-2026-000038",
            "KDH-2026-000035",
            "KDH-2026-000031",
            "Kiwi TCMS",
            "Praja",
            "Prospect",
            "EM ATENDIMENTO",
            "AGUARDANDO CLIENTE",
            "RESOLVIDO",
            "P1 — impacto crítico",
            "P2 — impacto alto",
            "P3 — impacto moderado",
            "P4 — dúvida ou solicitação sem impacto imediato",
        ):
            self.assertIn(expected, fixture)

    def test_functional_controller_uses_api_for_complete_ticket_flow(self):
        controller = (self.dist / "assets/js/portal-functional.js").read_text(encoding="utf-8")
        api = (self.dist / "assets/js/portal-api.js").read_text(encoding="utf-8")
        for expected in (
            "listProducts", "listTickets", "getTicket", "createTicket",
            "listMessages", "createMessage", "listEvents",
            "Carregando", "Nenhum chamado", "Não foi possível", "Enviando",
            "Anexos — próximo checkpoint.",
        ):
            self.assertIn(expected, controller + api)
        self.assertNotIn("organization_id", controller)
        self.assertNotIn("created_by_user_id", controller)
        self.assertNotIn("reference_code:", controller)

    def test_functional_pages_do_not_load_demo_fixture(self):
        for route in ("dashboard", "tickets", "detail", "new"):
            page = self.routes[route].read_text(encoding="utf-8")
            self.assertIn("/assets/js/portal-api.js", page)
            self.assertIn("/assets/js/portal-functional.js", page)
            self.assertNotIn("portal-demo-data.js", page)
            self.assertNotIn("portal-demo.js", page)
            self.assertIn("http://127.0.0.1:8011", page)

    def test_attachment_is_explicitly_disabled(self):
        controller = (self.dist / "assets/js/portal-functional.js").read_text(encoding="utf-8")
        self.assertIn("disabled: true", controller)
        self.assertIn("Anexos — próximo checkpoint.", controller)

    def test_demo_does_not_depend_on_backend_or_expose_sensitive_material(self):
        artifacts = [path.read_text(encoding="utf-8") for path in self.routes.values()]
        artifacts.extend(
            (self.dist / relative).read_text(encoding="utf-8")
            for relative in ("assets/js/portal-demo.js", "assets/js/portal-demo-data.js")
        )
        combined = "\n".join(artifacts).lower()
        for forbidden in (
            "fetch(",
            "xmlhttprequest",
            "localstorage",
            "sessionstorage",
            "authorization:",
            "access_token",
            "refresh_token",
            "client_secret",
            "database_url",
            "session_secret",
            "secret_key",
            "password",
            "jwt",
            "/api/",
        ):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
