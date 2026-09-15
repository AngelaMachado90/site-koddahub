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

  const normalize = (value) => String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .replace(/\s+/g, " ");

  const phraseInMessage = (message, phrase) => {
    if (!phrase) return false;
    return (` ${message} `).includes(` ${phrase} `);
  };

  function createConversation(pageContext = {}) {
    let lead = null;
    let lastTopic = "solução digital";
    let lastGlossary = null;
    const glossary = Array.isArray(pageContext.glossary) ? pageContext.glossary : [];
    const blogGlossary = Array.isArray(pageContext.blog_glossary) ? pageContext.blog_glossary : [];
    const glossaryCatalog = [...glossary, ...blogGlossary];

    function findGlossary(question) {
      const normalizedInput = normalize(question);
      const findIn = (items) => {
        const candidates = items.flatMap((item) => [item.term, item.normalized_term, ...(item.aliases || []), ...(item.normalized_aliases || [])]
          .map(normalize)
          .filter(Boolean)
          .map((key) => ({ item, key })))
          .sort((left, right) => right.key.length - left.key.length);
        return candidates.find(({ key }) => normalizedInput === key || phraseInMessage(normalizedInput, key))?.item;
      };
      return findIn(glossary) || findIn(blogGlossary);
    }

    function glossaryReply(item, expanded = false) {
      lastGlossary = item;
      lastTopic = item.term;
      const related = (item.related || []).filter((term) => glossaryCatalog.some((candidate) => normalize(candidate.term) === normalize(term))).slice(0, 3);
      return { kind: "glossary", intent: "GLOSSARY", term: item.term, text: item.definition, example: item.example, application: item.application, related, expanded };
    }

    function rememberArticle(href) {
      const topic = topics.find((item) => item.href === href);
      if (topic) lastTopic = topic.matches[0] === "n8n" ? "uma automação com n8n" : topic.label.replace(/^Ler (o guia|o artigo) sobre /, "");
    }

    function reply(question) {
      const value = String(question || "").trim();
      const normalized = normalize(value);
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
        return { intent: "COMMERCIAL_INTENT", text: `Ótimo! Podemos ajudar com ${lastTopic}. Para preparar seu contato com a equipe, preciso de três dados: nome, telefone e e-mail. Eles serão enviados somente se você confirmar a mensagem no WhatsApp. Qual é seu nome?`, lead: true };
      }
      if (/^(explique mais|ver exemplo|exemplo pratico)$/.test(normalized) && lastGlossary) return glossaryReply(lastGlossary, true);
      if (/diferenca entre dado e metrica/.test(normalized)) return { kind: "comparison", intent: "ARTICLE_QUESTION", text: "Dado é uma informação registrada. Métrica é uma medida calculada ou contada a partir de dados.", rows: [["Dado", "informação"], ["Métrica", "medida"]], related: ["Dado", "Métrica", "KPI"] };
      if (/diferenca entre metrica e kpi/.test(normalized)) return { kind: "comparison", intent: "ARTICLE_QUESTION", text: "Métrica é qualquer medida definida. KPI é a métrica escolhida para acompanhar um objetivo importante.", rows: [["Métrica", "medida"], ["KPI", "métrica ligada a um objetivo"]], related: ["Dado", "Métrica", "KPI"] };
      if (/zero.*(ausente|sem dado)|ausente.*zero/.test(normalized)) return { kind: "comparison", intent: "ARTICLE_QUESTION", text: "Não. Zero informa que nada ocorreu; dado ausente informa que não houve registro confiável.", rows: [["Zero", "nenhuma ocorrência"], ["Dado ausente", "informação não registrada"]], related: ["Valor zero", "Dado ausente"] };
      const glossaryItem = findGlossary(value);
      if (glossaryItem) return glossaryReply(glossaryItem);
      const topic = topics.find((item) => item.matches.some((word) => normalized.includes(word)));
      if (topic) {
        rememberArticle(topic.href);
        return { intent: "RELATED_CONTENT", text: topic.text, link: { href: topic.href, label: topic.label } };
      }
      return { kind: "unknown", intent: "UNKNOWN", text: pageContext.page_type === "blog" ? "Não encontrei esse termo no conteúdo que você está lendo. Posso explicar outro conceito do artigo ou ajudar você a encontrar um conteúdo relacionado." : "Não encontrei esse termo nos conteúdos disponíveis. Tente perguntar de outra forma ou procure um artigo relacionado." };
    }
    return { reply, rememberArticle };
  }

  return { createConversation, normalize, reply: createConversation().reply };
});
