(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root?.document) api.init(root);
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";
  const VIEW_TIMEOUT_MS = 5000;

  function canonicalUrl(document) {
    return document.querySelector('link[rel="canonical"]')?.href || document.location?.href || "";
  }

  function shouldIncrement(storage, slug) {
    const key = `koddahub:view:${slug}`;
    try {
      if (storage.getItem(key)) return false;
      storage.setItem(key, "1");
      return true;
    } catch (_) {
      return false;
    }
  }

  function formatViews(value) {
    return new Intl.NumberFormat("pt-BR").format(Number(value));
  }

  async function loadViews(root, element) {
    const slug = element.dataset.articleSlug || "";
    const endpoint = element.dataset.endpoint || "";
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug) || !endpoint) return;
    const increment = shouldIncrement(root.sessionStorage, slug);
    const controller = new AbortController();
    const timeout = root.setTimeout(() => controller.abort(), VIEW_TIMEOUT_MS);
    try {
      const response = await root.fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ article_slug: slug, increment }),
        signal: controller.signal,
        credentials: "same-origin"
      });
      if (!response.ok) return;
      const payload = await response.json();
      if (!payload.success || payload.article_slug !== slug || !Number.isSafeInteger(payload.views) || payload.views < 0) return;
      element.querySelector(".article-view-value").textContent = formatViews(payload.views);
    } catch (_) {
      element.hidden = true;
    } finally {
      root.clearTimeout(timeout);
    }
  }

  function initShare(root, share) {
    const url = canonicalUrl(root.document);
    const title = share.dataset.shareTitle || root.document.title;
    const text = share.dataset.shareText || title;
    const nativeButton = share.querySelector("[data-native-share]");
    const copyButton = share.querySelector("[data-copy-link]");
    const feedback = share.querySelector("[data-share-feedback]");
    share.querySelectorAll("[data-share-url]").forEach((link) => {
      const template = link.dataset.shareUrl;
      link.href = template.replace("{url}", encodeURIComponent(url)).replace("{title}", encodeURIComponent(title));
    });
    if (nativeButton && typeof root.navigator.share === "function") {
      nativeButton.hidden = false;
      nativeButton.addEventListener("click", async () => {
        try { await root.navigator.share({ title, text, url }); } catch (error) { if (error?.name !== "AbortError") nativeButton.hidden = true; }
      });
    }
    copyButton?.addEventListener("click", async () => {
      try {
        await root.navigator.clipboard.writeText(url);
        feedback.textContent = "Link copiado";
        root.setTimeout(() => { feedback.textContent = ""; }, 2500);
      } catch (_) {
        feedback.textContent = "Não foi possível copiar. Use o endereço do navegador.";
      }
    });
  }

  function init(root) {
    const share = root.document.querySelector(".article-share");
    if (share) initShare(root, share);
    const views = root.document.querySelector(".article-view-count");
    if (views) loadViews(root, views);
  }

  return { canonicalUrl, shouldIncrement, formatViews, loadViews, initShare, init };
});
