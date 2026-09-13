/* Respostas locais curtas enquanto o webhook da KoddaHub não está configurado. */
(function (root, factory) {
  const fallback = factory();
  root.koddaChatFallback = fallback;
  if (typeof module === "object" && module.exports) module.exports = fallback;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";

  const topics = [
    {
      matches: ["n8n", "workflow", "automatiz", "automacao"],
      text: "Para começar com n8n, defina a entrada, as regras, o resultado esperado e quem cuida das falhas. Nosso guia mostra um exemplo completo e os cuidados antes de colocar o fluxo em produção.",
      href: "/blog/n8n-na-pratica-quando-faz-sentido-automatizar-um-processo-com-a-ferramenta/",
      label: "Ler o guia sobre n8n"
    },
    {
      matches: ["responsiv", "celular", "mobile", "site"],
      text: "Um site responsivo precisa manter leitura, navegação e tarefas claras em cada tela. Veja o que validar no celular, tablet e desktop.",
      href: "/blog/site-responsivo-como-oferecer-uma-boa-experiencia-em-cada-tela/",
      label: "Ler o artigo sobre sites responsivos"
    },
    {
      matches: ["streamlit", "dashboard", "dados", "painel"],
      text: "Streamlit pode transformar uma análise em uma aplicação interativa. O artigo explica quando essa escolha ajuda e quais limites avaliar antes do uso recorrente.",
      href: "/blog/streamlit-quando-usar-para-transformar-dados-em-uma-aplicacao-util/",
      label: "Ler o artigo sobre Streamlit"
    },
    {
      matches: ["chatbot", "atendimento", "conversa", "cliente"],
      text: "Um chatbot pode responder perguntas repetidas, mas precisa preservar o contexto e saber quando encaminhar para uma pessoa. Veja como avaliar isso no atendimento.",
      href: "/blog/chatbot-no-atendimento-o-que-automatizar-sem-perder-o-contexto-da-conversa/",
      label: "Ler o guia sobre chatbot"
    }
  ];

  function reply(question) {
    const normalized = String(question || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    const topic = topics.find((item) => item.matches.some((word) => normalized.includes(word)));
    if (topic) return { text: topic.text, link: { href: topic.href, label: topic.label } };
    return { text: "Posso indicar leituras sobre n8n, sites responsivos, Streamlit e chatbots. Escreva um desses temas ou fale com nossa equipe pelo WhatsApp abaixo." };
  }

  return { reply };
});
