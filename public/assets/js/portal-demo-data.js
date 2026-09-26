(function (root) {
  "use strict";

  const data = Object.freeze({
    persona: Object.freeze({
      name: "Marina Costa",
      organization: "Empresa Demonstração",
      role: "Cliente",
    }),
    products: Object.freeze(["Kiwi TCMS", "Praja", "Prospect"]),
    priorities: Object.freeze([
      Object.freeze({ value: "P1", label: "P1 — impacto crítico" }),
      Object.freeze({ value: "P2", label: "P2 — impacto alto" }),
      Object.freeze({ value: "P3", label: "P3 — impacto moderado" }),
      Object.freeze({ value: "P4", label: "P4 — dúvida ou solicitação sem impacto imediato" }),
    ]),
    metrics: Object.freeze([
      Object.freeze({ label: "Chamados abertos", value: 2, tone: "brand" }),
      Object.freeze({ label: "Aguardando cliente", value: 1, tone: "warning" }),
      Object.freeze({ label: "Resolvidos", value: 3, tone: "success" }),
    ]),
    tickets: Object.freeze([
      Object.freeze({
        number: "KDH-2026-000042",
        product: "Kiwi TCMS",
        subject: "Dúvida sobre execução de caso de teste",
        priority: "P3",
        status: "in_progress",
        statusLabel: "EM ATENDIMENTO",
        updatedAt: "25/09/2026 16:05",
        href: "/portal/demo/chamados/KDH-2026-000042/",
      }),
      Object.freeze({
        number: "KDH-2026-000041",
        product: "Kiwi TCMS",
        subject: "Usuário sem acesso ao projeto",
        priority: "P2",
        status: "waiting_customer",
        statusLabel: "AGUARDANDO CLIENTE",
        updatedAt: "25/09/2026 15:48",
        href: null,
      }),
      Object.freeze({
        number: "KDH-2026-000038",
        product: "Kiwi TCMS",
        subject: "Dúvida sobre evidências",
        priority: "P4",
        status: "resolved",
        statusLabel: "RESOLVIDO",
        updatedAt: "24/09/2026 11:20",
        href: null,
      }),
      Object.freeze({
        number: "KDH-2026-000035",
        product: "Praja",
        subject: "Dúvida sobre importação de contatos",
        priority: "P3",
        status: "closed",
        statusLabel: "ENCERRADO",
        updatedAt: "23/09/2026 17:40",
        href: null,
      }),
      Object.freeze({
        number: "KDH-2026-000031",
        product: "Prospect",
        subject: "Consulta sobre processamento de leads",
        priority: "P3",
        status: "resolved",
        statusLabel: "RESOLVIDO",
        updatedAt: "22/09/2026 10:15",
        href: null,
      }),
    ]),
    featuredTicket: Object.freeze({
      number: "KDH-2026-000042",
      product: "Kiwi TCMS",
      subject: "Dúvida sobre execução de caso de teste",
      priority: "P3",
      status: "in_progress",
      statusLabel: "EM ATENDIMENTO",
      createdAt: "25/09/2026 14:32",
      description: "Olá, estou com uma dúvida sobre como iniciar uma nova execução a partir de um caso de teste existente no Kiwi TCMS.",
      interactions: Object.freeze([
        Object.freeze({ at: "25/09/2026 14:32", author: "Marina Costa", message: "Chamado aberto.", customer: true }),
        Object.freeze({ at: "25/09/2026 15:10", author: "Suporte KoddaHub", message: "Recebemos sua solicitação e estamos analisando o cenário informado.", customer: false }),
        Object.freeze({ at: "25/09/2026 16:05", author: "Suporte KoddaHub", message: "Identificamos o fluxo correto para iniciar a execução diretamente pelo caso de teste.", customer: false }),
      ]),
    }),
  });

  root.PortalDemoData = data;
  if (typeof module !== "undefined" && module.exports) module.exports = data;
})(typeof window !== "undefined" ? window : globalThis);
