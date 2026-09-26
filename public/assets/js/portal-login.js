(function () {
  "use strict";

  const form = document.getElementById("portalLoginForm");
  const password = document.getElementById("password");
  const toggle = document.querySelector("[data-password-toggle]");
  const status = document.getElementById("loginStatus");

  if (!form || !password || !toggle || !status) return;

  toggle.addEventListener("click", () => {
    const showing = password.type === "text";
    password.type = showing ? "password" : "text";
    toggle.setAttribute("aria-pressed", String(!showing));
    toggle.setAttribute("aria-label", showing ? "Mostrar senha" : "Ocultar senha");
    toggle.querySelector("span").textContent = showing ? "Mostrar" : "Ocultar";
    password.focus({ preventScroll: true });
  });

  document.querySelectorAll("[data-auth-provider]").forEach((button) => {
    button.addEventListener("click", () => {
      const provider = button.dataset.authProvider;
      status.textContent = `A entrada com ${provider === "google" ? "Google" : "LinkedIn"} será disponibilizada após a integração segura do Portal KoddaHub.`;
    });
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    status.textContent = "A autenticação estará disponível no próximo checkpoint do Portal KoddaHub.";
  });
})();
