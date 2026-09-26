import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PortalLoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "public/index.template.html").read_text(encoding="utf-8")
        cls.login = (ROOT / "public/portal/login/index.template.html").read_text(encoding="utf-8")
        cls.script = (ROOT / "public/assets/js/portal-login.js").read_text(encoding="utf-8")

    def test_header_exposes_portal_without_changing_whatsapp_target(self):
        self.assertIn('href="/portal/login/"', self.home)
        self.assertIn('href="https://wa.me/5541992272854?', self.home)

    def test_login_has_accessible_fields_and_future_routes(self):
        self.assertIn('<label class="form-label" for="email">', self.login)
        self.assertIn('autocomplete="email"', self.login)
        self.assertIn('<label class="form-label" for="password">', self.login)
        self.assertIn('autocomplete="current-password"', self.login)
        self.assertIn('aria-label="Mostrar senha"', self.login)
        self.assertIn('role="status" aria-live="polite"', self.login)
        self.assertIn('href="/portal/recuperar-senha/"', self.login)
        self.assertIn('href="/portal/cadastro/"', self.login)

    def test_providers_are_structural_and_authentication_is_not_simulated(self):
        self.assertIn('data-auth-provider="google"', self.login)
        self.assertIn('data-auth-provider="linkedin"', self.login)
        for forbidden in ("fetch(", "localStorage", "sessionStorage", "access_token", "client_secret"):
            self.assertNotIn(forbidden, self.script)


if __name__ == "__main__":
    unittest.main()
