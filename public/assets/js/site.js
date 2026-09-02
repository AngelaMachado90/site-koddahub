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

  const motionReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const animatedGroups = document.querySelectorAll(".section-heading, .service-grid, .process-heading, .process-list, .case-grid, .map-frame, .contact-content, .contact-closing");

  if (motionReduced || !("IntersectionObserver" in window)) {
    animatedGroups.forEach((element) => element.classList.add("is-visible"));
    return;
  }

  document.body.classList.add("motion-ready");
  animatedGroups.forEach((element) => element.classList.add("reveal"));

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -10%", threshold: 0.12 });

  animatedGroups.forEach((element) => revealObserver.observe(element));
})();
