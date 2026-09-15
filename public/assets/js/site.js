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

/* Chat de atendimento: o endpoint e injetado pelo build conforme o ambiente. */
(function () {
  "use strict";

  const CHAT_WEBHOOK_URL = document.querySelector('meta[name="koddahub-chat-webhook-url"]')?.content.trim() || "";
  const SESSION_KEY = "kodda_chat_session_id";
  const MESSAGES_KEY = "kodda_chat_messages";
  const MAX_MESSAGES = 50;
  const REQUEST_TIMEOUT = 20000;
  const HAS_REMOTE_AGENT = Boolean(CHAT_WEBHOOK_URL);
  const PAGE_CONTEXT = (() => {
    try { return JSON.parse(document.getElementById("kodda-page-context")?.textContent || "{}"); }
    catch (_) { return {}; }
  })();
  const WELCOME_MESSAGE = HAS_REMOTE_AGENT
    ? "Olá! Sou a Kodda. Posso ajudar a explicar este conteúdo."
    : PAGE_CONTEXT.page_type === "blog" ? "Olá! Posso explicar os conceitos deste artigo." : "Olá! Posso ajudar a descomplicar os conteúdos do Blog Koddahub.";
  const LEGACY_ERROR_MESSAGE = "Não consegui responder agora. Tente novamente em alguns instantes.";
  const ERROR_MESSAGE = "Não consegui responder agora. Sua pergunta continua no campo para tentar de novo. Você também pode falar com nossa equipe pelo WhatsApp abaixo.";

  const trigger = document.querySelector(".kodda-chat-trigger");
  const panel = document.getElementById("koddaChatPanel");
  const description = panel?.querySelector("#koddaChatDescription");
  const closeButton = panel?.querySelector(".kodda-chat-close");
  const messagesElement = panel?.querySelector(".kodda-chat-messages");
  const form = panel?.querySelector(".kodda-chat-form");
  const input = panel?.querySelector(".kodda-chat-input");
  const sendButton = panel?.querySelector(".kodda-chat-send");
  const ctaContext = panel?.querySelector(".kodda-chat-cta-context");
  if (!trigger || !panel || !closeButton || !messagesElement || !form || !input || !sendButton) return;
  if (!HAS_REMOTE_AGENT) {
    document.querySelector(".kodda-chat")?.classList.add("kodda-chat-local");
    if (description) description.textContent = PAGE_CONTEXT.page_type === "blog" ? "Explicando este artigo" : "Descomplicando tecnologia";
  }

  let isSending = false;
  let messages = loadMessages();
  const localConversation = window.koddaChatFallback?.createConversation(PAGE_CONTEXT);
  const lastArticle = [...messages].reverse().find((message) => message.link?.href);
  if (lastArticle) localConversation?.rememberArticle(lastArticle.link.href);

  function readStorage(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value === null ? fallback : value;
    } catch (_) {
      return fallback;
    }
  }

  function getSessionId() {
    const savedId = readStorage(SESSION_KEY, "");
    if (savedId) return savedId;
    const id = typeof crypto.randomUUID === "function"
      ? crypto.randomUUID()
      : `kodda-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    try { localStorage.setItem(SESSION_KEY, id); } catch (_) { /* Storage pode estar indisponível. */ }
    return id;
  }

  function loadMessages() {
    try {
      const saved = JSON.parse(readStorage(MESSAGES_KEY, "[]"));
      if (!Array.isArray(saved)) return [];
      return saved.filter((item) => item && ["user", "assistant"].includes(item.role) && typeof item.text === "string" && item.text !== LEGACY_ERROR_MESSAGE)
        .map((item) => ({
          role: item.role,
          text: item.text,
          timestamp: item.timestamp,
          link: item.link && typeof item.link.href === "string" && /^\/blog\/[a-z0-9-]+\/$/.test(item.link.href) && typeof item.link.label === "string" ? item.link : undefined
        })).slice(-MAX_MESSAGES);
    } catch (_) {
      return [];
    }
  }

  function persistMessages() {
    messages = messages.slice(-MAX_MESSAGES);
    try { localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages)); } catch (_) { /* O chat continua sem persistência. */ }
  }

  function formatTime(date) {
    return new Intl.DateTimeFormat("pt-BR", { hour: "2-digit", minute: "2-digit" }).format(date);
  }

  function scrollChatToBottom() {
    requestAnimationFrame(() => { messagesElement.scrollTop = messagesElement.scrollHeight; });
  }

  function addMessage(text, role, options = {}) {
    const message = document.createElement("div");
    message.className = `kodda-message kodda-message-${role}`;
    if (options.typing) {
      message.classList.add("kodda-message-typing");
      message.setAttribute("aria-label", "Kodda está explicando");
      for (let index = 0; index < 3; index += 1) message.append(document.createElement("span"));
    } else {
      const content = document.createElement("p");
      const time = document.createElement("time");
      let extraDetail = null;
      const timestamp = options.timestamp ? new Date(options.timestamp) : new Date();
      content.textContent = text;
      if (options.answer?.kind === "glossary") {
        message.classList.add("kodda-chat-glossary-card");
        const title = document.createElement("strong");
        title.className = "kodda-chat-term";
        title.textContent = options.answer.term;
        message.prepend(title);
        if (options.answer.expanded) {
          const example = document.createElement("div");
          example.className = "kodda-chat-example";
          example.innerHTML = `<strong>Exemplo</strong><span></span><strong>Para que serve</strong><span></span>`;
          example.children[1].textContent = options.answer.example;
          example.children[3].textContent = options.answer.application;
          extraDetail = example;
        }
      } else if (options.answer?.kind === "comparison") {
        message.classList.add("kodda-chat-glossary-card");
        const comparison = document.createElement("dl");
        comparison.className = "kodda-chat-comparison";
        (options.answer.rows || []).forEach(([term, meaning]) => {
          const dt = document.createElement("dt"); dt.textContent = term;
          const dd = document.createElement("dd"); dd.textContent = meaning;
          comparison.append(dt, dd);
        });
        extraDetail = comparison;
      }
      if (options.link) {
        const link = document.createElement("a");
        link.className = "kodda-message-link";
        link.href = options.link.href;
        link.textContent = `${options.link.label} →`;
        if (link.hostname === "wa.me") {
          link.target = "_blank";
          link.rel = "noopener";
        }
        message.append(content, link, time);
      } else {
        message.append(content, time);
      }
      if (extraDetail) message.insertBefore(extraDetail, time);
      const actions = options.answer?.kind === "glossary" && !options.answer.expanded
        ? ["Ver exemplo", "Explique mais", ...(options.answer.related || [])]
        : (options.answer?.related || []);
      if (actions.length) message.insertBefore(quickReplies(actions), time);
      time.dateTime = timestamp.toISOString();
      time.textContent = formatTime(timestamp);
      if (options.persist !== false) {
        messages.push({ role, text, timestamp: timestamp.toISOString(), link: options.link });
        persistMessages();
      }
    }
    messagesElement.append(message);
    scrollChatToBottom();
    return message;
  }

  function quickReplies(labels) {
    const group = document.createElement("div");
    group.className = "kodda-chat-quick-replies";
    group.setAttribute("aria-label", "Sugestões de perguntas");
    labels.slice(0, 5).forEach((label) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "btn btn-sm kodda-chat-quick-reply";
      button.textContent = label;
      button.addEventListener("click", () => { input.value = label; resizeInput(); sendMessage(); });
      group.append(button);
    });
    return group;
  }

  function updateContextualCta(answer) {
    if (!ctaContext || answer?.kind !== "glossary") return;
    ctaContext.textContent = PAGE_CONTEXT.article_category === "Dados"
      ? "Quer organizar os indicadores do seu negócio?"
      : "Quer aplicar este conceito no seu negócio?";
    ctaContext.hidden = false;
  }

  function renderHistory() {
    messagesElement.textContent = "";
    if (!messages.length) {
      addMessage(WELCOME_MESSAGE, "assistant");
      const suggestions = (PAGE_CONTEXT.glossary || []).slice(0, 3).map((item) => item.term);
      if (suggestions.length) messagesElement.lastElementChild?.append(quickReplies(suggestions));
      return;
    }
    messages.forEach((message) => addMessage(message.text, message.role, { timestamp: message.timestamp, link: message.link, persist: false }));
    if (!HAS_REMOTE_AGENT && messages.at(-1)?.role === "user") {
      const answer = localReply(messages.at(-1).text);
      addMessage(answer.text, "assistant", { link: answer.link });
    }
    scrollChatToBottom();
  }

  function resizeInput() {
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, 120)}px`;
  }

  function openChat() {
    if (!panel.hidden) return;
    panel.hidden = false;
    trigger.hidden = true;
    trigger.setAttribute("aria-expanded", "true");
    document.body.classList.add("kodda-chat-open");
    requestAnimationFrame(() => panel.classList.add("is-open"));
    scrollChatToBottom();
    setTimeout(() => input.focus({ preventScroll: true }), 150);
  }

  function closeChat() {
    if (panel.hidden) return;
    panel.classList.remove("is-open");
    panel.hidden = true;
    trigger.hidden = false;
    trigger.setAttribute("aria-expanded", "false");
    document.body.classList.remove("kodda-chat-open");
    trigger.focus({ preventScroll: true });
  }

  async function sendMessageToAgent(message) {
    if (!CHAT_WEBHOOK_URL) throw new Error("Webhook do chat não configurado");
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);
    try {
      const response = await fetch(CHAT_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, sessionId: getSessionId(), context: { page_type: PAGE_CONTEXT.page_type || "site", page_url: location.href, article_slug: PAGE_CONTEXT.article_slug, article_title: PAGE_CONTEXT.article_title, article_category: PAGE_CONTEXT.article_category } }),
        signal: controller.signal
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const answer = typeof data.output === "string" ? data.output : data.message;
      if (typeof answer !== "string" || !answer.trim()) throw new Error("Resposta vazia");
      return { text: answer.trim() };
    } finally {
      clearTimeout(timeoutId);
    }
  }

  function localReply(message) {
    return localConversation?.reply(message) || {
      text: "O atendimento automático está indisponível. Fale com nossa equipe pelo WhatsApp abaixo."
    };
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text || isSending) return;
    isSending = true;
    input.value = "";
    resizeInput();
    input.disabled = true;
    sendButton.disabled = true;
    const localAnswer = HAS_REMOTE_AGENT ? null : localReply(text);
    addMessage(text, "user", { persist: !localAnswer?.lead });
    const typing = HAS_REMOTE_AGENT ? addMessage("", "assistant", { typing: true, persist: false }) : null;
    try {
      const answer = HAS_REMOTE_AGENT ? await sendMessageToAgent(text) : localAnswer;
      typing?.remove();
      updateContextualCta(answer);
      addMessage(answer.text, "assistant", { link: answer.link, answer, persist: !answer.lead });
    } catch (error) {
      console.error("Falha ao enviar mensagem ao agente:", error);
      typing?.remove();
      input.value = text;
      resizeInput();
      const errorMessage = addMessage(ERROR_MESSAGE, "assistant", { persist: false });
      errorMessage.classList.add("kodda-chat-error");
      const retry = document.createElement("button");
      retry.type = "button";
      retry.className = "btn btn-sm kodda-chat-quick-reply mt-2";
      retry.textContent = "Tentar novamente";
      retry.addEventListener("click", () => { input.value = text; resizeInput(); input.focus(); });
      errorMessage.append(retry);
    } finally {
      isSending = false;
      input.disabled = false;
      sendButton.disabled = false;
      input.focus({ preventScroll: true });
    }
  }

  renderHistory();
  getSessionId();
  trigger.addEventListener("click", openChat);
  closeButton.addEventListener("click", closeChat);
  form.addEventListener("submit", (event) => { event.preventDefault(); sendMessage(); });
  input.addEventListener("input", resizeInput);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      sendMessage();
    }
  });
  document.addEventListener("click", (event) => {
    const button = event.target.closest?.(".glossary-ask-kodda");
    if (!button) return;
    openChat();
    input.value = button.dataset.glossaryTerm || "";
    resizeInput();
    sendMessage();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden && window.matchMedia("(min-width: 576px)").matches) closeChat();
  });
})();
