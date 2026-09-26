(function (root) {
  "use strict";
  const base = (root.document?.querySelector('meta[name="portal-api-base-url"]')?.content || "").replace(/\/$/, "");
  async function request(path, options = {}) {
    const controller = new AbortController();
    const timer = root.setTimeout(() => controller.abort(), 10000);
    try {
      const response = await root.fetch(base + path, { ...options, headers: { "Content-Type": "application/json" }, signal: controller.signal });
      const data = await response.json().catch(() => null);
      if (!response.ok) throw new Error(data?.detail || "Não foi possível concluir a solicitação.");
      return data;
    } catch (error) {
      if (error.name === "AbortError") throw new Error("A API demorou para responder.");
      throw error;
    } finally { root.clearTimeout(timer); }
  }
  root.PortalAPI = Object.freeze({
    health: () => request("/health"), listProducts: () => request("/api/products"), listTickets: () => request("/api/tickets"),
    getTicket: (id) => request(`/api/tickets/${encodeURIComponent(id)}`),
    createTicket: (data) => request("/api/tickets", { method: "POST", body: JSON.stringify(data) }),
    listMessages: (id) => request(`/api/tickets/${encodeURIComponent(id)}/messages`),
    createMessage: (id, data) => request(`/api/tickets/${encodeURIComponent(id)}/messages`, { method: "POST", body: JSON.stringify(data) }),
    listEvents: (id) => request(`/api/tickets/${encodeURIComponent(id)}/events`),
  });
})(window);
