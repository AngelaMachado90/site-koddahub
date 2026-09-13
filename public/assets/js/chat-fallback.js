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

  function createConversation() {
    let lead = null;
    let lastTopic = "solução digital";

    function rememberArticle(href) {
      const topic = topics.find((item) => item.href === href);
      if (topic) lastTopic = topic.matches[0] === "n8n" ? "uma automação com n8n" : topic.label.replace(/^Ler (o guia|o artigo) sobre /, "");
    }

    function reply(question) {
      const value = String(question || "").trim();
      const normalized = value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
      if (lead) {
        if (lead.step === "name") {
          if (!/^[\p{L}][\p{L}\s.'-]{1,79}$/u.test(value)) return { text: "Informe seu nome para continuar (pelo menos duas letras).", lead: true };
          lead.name = value;
          lead.step = "phone";
          return { text: `Obrigado, ${value}. Qual é seu telefone com DDD?`, lead: true };
        }
        if (lead.step === "phone") {
          const digits = value.replace(/\D/g, "");
          if (digits.length < 10 || digits.length > 11) return { text: "Informe um telefone com DDD, com 10 ou 11 dígitos.", lead: true };
          lead.phone = digits;
          lead.step = "email";
          return { text: "E qual é seu e-mail?", lead: true };
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || value.length > 254) return { text: "Confira o e-mail e tente novamente. Exemplo: nome@empresa.com.br", lead: true };
        const summary = `Olá! Vim pelo site da KoddaHub e gostaria de implementar ${lead.topic} na minha empresa.\nNome: ${lead.name}\nTelefone: ${lead.phone}\nE-mail: ${value}`;
        lead = null;
        return {
          text: "Pronto! Toque no botão abaixo para enviar seus dados à nossa equipe pelo WhatsApp. A mensagem só será enviada quando você confirmar no WhatsApp.",
          link: { href: `https://wa.me/5541992272854?text=${encodeURIComponent(summary)}`, label: "Enviar à equipe pelo WhatsApp" },
          lead: true
        };
      }
      if (/(implement|implant|contrat|orcament|proposta|minha empresa|meu negocio|meu neg[oó]cio|preciso de ajuda|quero fazer)/.test(normalized)) {
        lead = { step: "name", topic: lastTopic };
        return { text: `Ótimo! Podemos ajudar com ${lastTopic}. Para preparar seu contato com a equipe, preciso de três dados: nome, telefone e e-mail. Eles serão enviados somente se você confirmar a mensagem no WhatsApp. Qual é seu nome?`, lead: true };
      }
      const topic = topics.find((item) => item.matches.some((word) => normalized.includes(word)));
      if (topic) {
        rememberArticle(topic.href);
        return { text: topic.text, link: { href: topic.href, label: topic.label } };
      }
      return { text: "Posso indicar leituras sobre n8n, sites responsivos, Streamlit e chatbots. Se quiser implementar uma solução na sua empresa, diga 'quero implementar' ou fale com nossa equipe pelo WhatsApp abaixo." };
    }
    return { reply, rememberArticle };
  }

  return { createConversation, reply: createConversation().reply };
});
