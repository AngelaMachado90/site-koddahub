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
  const WELCOME_MESSAGE = "Olá! Sou a Kodda, assistente da KoddaHub. Como posso ajudar?";
  const ERROR_MESSAGE = "Não consegui responder agora. Tente novamente em alguns instantes.";

  const trigger = document.querySelector(".kodda-chat-trigger");
  const panel = document.getElementById("koddaChatPanel");
  const closeButton = panel?.querySelector(".kodda-chat-close");
  const messagesElement = panel?.querySelector(".kodda-chat-messages");
  const form = panel?.querySelector(".kodda-chat-form");
  const input = panel?.querySelector(".kodda-chat-input");
  const sendButton = panel?.querySelector(".kodda-chat-send");
  if (!trigger || !panel || !closeButton || !messagesElement || !form || !input || !sendButton) return;

  let isSending = false;
  let messages = loadMessages();

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
      return saved.filter((item) => item && ["user", "assistant"].includes(item.role) && typeof item.text === "string").slice(-MAX_MESSAGES);
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
      message.setAttribute("aria-label", "Kodda está digitando");
      for (let index = 0; index < 3; index += 1) message.append(document.createElement("span"));
    } else {
      const content = document.createElement("p");
      const time = document.createElement("time");
      const timestamp = options.timestamp ? new Date(options.timestamp) : new Date();
      content.textContent = text;
      time.dateTime = timestamp.toISOString();
      time.textContent = formatTime(timestamp);
      message.append(content, time);
      if (options.persist !== false) {
        messages.push({ role, text, timestamp: timestamp.toISOString() });
        persistMessages();
      }
    }
    messagesElement.append(message);
    scrollChatToBottom();
    return message;
  }

  function renderHistory() {
    messagesElement.textContent = "";
    if (!messages.length) {
      addMessage(WELCOME_MESSAGE, "assistant");
      return;
    }
    messages.forEach((message) => addMessage(message.text, message.role, { timestamp: message.timestamp, persist: false }));
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
        body: JSON.stringify({ message, sessionId: getSessionId() }),
        signal: controller.signal
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const answer = typeof data.output === "string" ? data.output : data.message;
      if (typeof answer !== "string" || !answer.trim()) throw new Error("Resposta vazia");
      return answer.trim();
    } finally {
      clearTimeout(timeoutId);
    }
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text || isSending) return;
    isSending = true;
    input.value = "";
    resizeInput();
    input.disabled = true;
    sendButton.disabled = true;
    addMessage(text, "user");
    const typing = addMessage("", "assistant", { typing: true, persist: false });
    try {
      const answer = await sendMessageToAgent(text);
      typing.remove();
      addMessage(answer, "assistant");
    } catch (error) {
      console.error("Falha ao enviar mensagem ao agente:", error);
      typing.remove();
      addMessage(ERROR_MESSAGE, "assistant");
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
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden && window.matchMedia("(min-width: 576px)").matches) closeChat();
  });
})();
