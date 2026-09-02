(function () {
  "use strict";
  const header = document.querySelector(".site-header");
  const menu = document.getElementById("mainNav");
  const updateHeader = () => header && header.classList.toggle("is-scrolled", window.scrollY > 16);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
  if (!menu || typeof bootstrap === "undefined") return;
  menu.querySelectorAll("a[href^='#']").forEach((link) => link.addEventListener("click", () => {
    if (window.matchMedia("(max-width: 991.98px)").matches && menu.classList.contains("show")) bootstrap.Collapse.getOrCreateInstance(menu).hide();
  }));
})();
