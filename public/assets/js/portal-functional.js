(function (root) {
  "use strict";
  const d = root.document, api = root.PortalAPI, container = d.getElementById("demoPageContent"), page = d.body.dataset.demoPage;
  if (!api || !container) return;
  const el = (tag, cls, text) => { const n = d.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; };
  const date = (v) => new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(new Date(v));
  const href = (t) => `/portal/demo/chamados/detalhe/?id=${encodeURIComponent(t.id)}`;
  function link(text, url, primary) { const n = el("a", primary ? "btn btn-brand" : "demo-action-link", text); n.href = url; return n; }
  function header(title, copy, action) { const h = el("header", "demo-page-head"), box = el("div"); box.append(el("h1", "", title), el("p", "", copy)); h.append(box); if (action) h.append(action); return h; }
  function state(kind, text, retry) { const n = el("div", `demo-card demo-panel demo-state demo-state--${kind}`); n.setAttribute("role", kind === "error" ? "alert" : "status"); n.append(el("p", "", text)); if (retry) { const b = el("button", "btn btn-brand", "Tentar novamente"); b.onclick = retry; n.append(b); } return n; }
  function table(tickets) {
    const shell = el("div", "demo-table-shell"), table = el("table", "table demo-table"), head = el("tr");
    ["Número", "Produto", "Assunto", "Prioridade", "Status", "Atualizado em", "Ação"].forEach((x) => head.append(el("th", "", x)));
    const body = el("tbody"); tickets.forEach((t) => { const row = el("tr"); [t.reference_code, t.product_name, t.title, t.priority.toUpperCase(), t.status.replaceAll("_", " ").toUpperCase(), date(t.updated_at)].forEach((x, i) => { const c = el("td", "", x); c.dataset.label = head.children[i].textContent; row.append(c); }); const c = el("td"); c.append(link("Ver detalhes", href(t))); row.append(c); body.append(row); });
    const thead = el("thead"); thead.append(head); table.append(thead, body); shell.append(table); return shell;
  }
  async function tickets(dashboard) {
    container.replaceChildren(state("loading", "Carregando chamados…"));
    try { const items = await api.listTickets(); container.replaceChildren(header(dashboard ? "Portal de Suporte" : "Meus chamados", "Dados persistidos no ambiente HML.", link("Abrir chamado", "/portal/demo/chamados/novo/", true))); container.append(items.length ? table(items) : state("empty", "Nenhum chamado encontrado.")); }
    catch (_) { container.replaceChildren(state("error", "Não foi possível carregar os chamados.", () => tickets(dashboard))); }
  }
  function field(label, control) { const w = el("div", "col-12"); w.append(el("label", "form-label", label), control); return w; }
  async function newTicket() {
    container.replaceChildren(state("loading", "Carregando produtos…"));
    try {
      const products = await api.listProducts(), form = el("form", "demo-form row g-3"), select = el("select", "form-select"); select.required = true;
      select.append(Object.assign(el("option", "", "Selecione um produto"), { value: "" })); products.forEach((p) => select.append(Object.assign(el("option", "", p.name), { value: p.id })));
      const title = Object.assign(el("input", "form-control"), { required: true, maxLength: 160 }), priority = el("select", "form-select"), message = Object.assign(el("textarea", "form-control"), { required: true, maxLength: 10000 });
      ["p1", "p2", "p3", "p4"].forEach((p) => priority.append(Object.assign(el("option", "", p.toUpperCase()), { value: p })));
      const attachment = Object.assign(el("input", "form-control"), { type: "file", disabled: true }), attach = field("Anexo", attachment); attach.append(el("p", "demo-help", "Anexos — próximo checkpoint."));
      const submit = Object.assign(el("button", "btn btn-brand", "Abrir chamado"), { type: "submit" }), feedback = el("p", "demo-feedback");
      form.append(field("Produto", select), field("Assunto", title), field("Prioridade", priority), field("Descrição", message), attach, submit, feedback);
      form.onsubmit = async (event) => { event.preventDefault(); if (!form.reportValidity()) return; submit.disabled = true; submit.textContent = "Enviando…"; try { const t = await api.createTicket({ product_id: Number(select.value), title: title.value.trim(), priority: priority.value, message: message.value.trim() }); feedback.textContent = `Chamado ${t.reference_code} criado. `; feedback.append(link("Abrir", href(t))); form.reset(); } catch (e) { feedback.textContent = e.message; } finally { submit.disabled = false; submit.textContent = "Abrir chamado"; } };
      const panel = el("section", "demo-card demo-panel"); panel.append(form); container.replaceChildren(header("Abrir chamado", "Persistência real no HML."), panel);
    } catch (_) { container.replaceChildren(state("error", "Não foi possível carregar os produtos.", newTicket)); }
  }
  async function detail() {
    const id = new URLSearchParams(root.location.search).get("id"); if (!id) return container.replaceChildren(state("error", "Chamado não informado.")); container.replaceChildren(state("loading", "Carregando chamado…"));
    try {
      const [t, messages, events] = await Promise.all([api.getTicket(id), api.listMessages(id), api.listEvents(id)]), info = el("dl", "demo-detail-grid");
      [["Produto", t.product_name], ["Prioridade", t.priority.toUpperCase()], ["Status", t.status.toUpperCase()], ["Criado em", date(t.created_at)]].forEach(([a, b]) => { const w = el("div"); w.append(el("dt", "", a), el("dd", "", b)); info.append(w); });
      const history = el("section", "demo-card demo-panel demo-section"), list = el("ol", "demo-timeline"); history.append(el("h2", "", "Mensagens")); messages.forEach((m) => { const i = el("li"); i.append(el("time", "", date(m.created_at)), el("strong", "", m.author_name), el("p", "", m.body)); list.append(i); }); history.append(list);
      const timeline = el("section", "demo-card demo-panel demo-section"), eventList = el("ol", "demo-timeline"); timeline.append(el("h2", "", "Eventos")); events.forEach((e) => { const i = el("li"); i.append(el("time", "", date(e.created_at)), el("strong", "", e.event_type)); eventList.append(i); }); timeline.append(eventList);
      const response = el("section", "demo-card demo-panel demo-section"), form = el("form", "demo-form"), body = Object.assign(el("textarea", "form-control"), { required: true }), submit = Object.assign(el("button", "btn btn-brand mt-3", "Enviar resposta"), { type: "submit" }), feedback = el("p", "demo-feedback"); response.append(el("h2", "", "Responder chamado")); form.append(body, submit, feedback); response.append(form);
      form.onsubmit = async (event) => { event.preventDefault(); if (!form.reportValidity()) return; submit.disabled = true; try { await api.createMessage(id, { body: body.value.trim() }); await detail(); } catch (e) { feedback.textContent = e.message; submit.disabled = false; } };
      container.replaceChildren(link("← Meus chamados", "/portal/demo/chamados/"), header(t.reference_code, t.title), info, history, timeline, response);
    } catch (_) { container.replaceChildren(state("error", "Não foi possível carregar o chamado.", detail)); }
  }
  const active = page === "ticket-detail" ? "chamados" : page; d.querySelector(`[data-demo-nav="${active}"]`)?.setAttribute("aria-current", "page");
  if (page === "dashboard") tickets(true); else if (page === "chamados") tickets(false); else if (page === "new-ticket") newTicket(); else if (page === "ticket-detail") detail();
})(window);
