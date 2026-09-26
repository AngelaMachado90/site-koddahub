(function (root) {
  "use strict";
  const documentRef = root.document;
  const data = root.PortalDemoData;
  if (!documentRef || !data) return;

  function element(tag, className, text) {
    const node = documentRef.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function pageHeader(title, description, action) {
    const header = element("header", "demo-page-head");
    const copy = element("div");
    copy.append(element("h1", "", title), element("p", "", description));
    header.append(copy);
    if (action) header.append(action);
    return header;
  }

  function actionLink(label, href, primary) {
    const link = element("a", primary ? "btn btn-brand" : "demo-action-link", label);
    link.href = href;
    return link;
  }

  function statusBadge(ticket) {
    return element("span", `demo-status demo-status--${ticket.status}`, ticket.statusLabel);
  }

  function priorityBadge(priority) {
    return element("span", "demo-priority", priority);
  }

  function ticketNumber(ticket) {
    if (!ticket.href) return element("span", "demo-ticket-number", ticket.number);
    const link = actionLink(ticket.number, ticket.href, false);
    link.className = "demo-ticket-number";
    link.setAttribute("aria-label", "Ver detalhes do chamado " + ticket.number);
    return link;
  }

  function ticketTable(tickets) {
    const shell = element("div", "demo-table-shell");
    const table = element("table", "table demo-table");
    const caption = element("caption", "visually-hidden", "Lista de chamados demonstrativos");
    const head = element("thead");
    const headRow = element("tr");
    ["Número", "Produto", "Assunto", "Prioridade", "Status", "Atualizado em", "Ação"].forEach((label) => {
      const cell = element("th", "", label);
      cell.scope = "col";
      headRow.append(cell);
    });
    head.append(headRow);
    const body = element("tbody");
    tickets.forEach((ticket) => {
      const row = element("tr");
      const values = [
        ticketNumber(ticket),
        documentRef.createTextNode(ticket.product),
        element("span", "demo-ticket-subject", ticket.subject),
        priorityBadge(ticket.priority),
        statusBadge(ticket),
        documentRef.createTextNode(ticket.updatedAt),
      ];
      const labels = ["Número", "Produto", "Assunto", "Prioridade", "Status", "Atualizado em"];
      values.forEach((value, index) => {
        const cell = element("td");
        cell.dataset.label = labels[index];
        cell.append(value);
        row.append(cell);
      });
      const actionCell = element("td");
      actionCell.dataset.label = "Ação";
      if (ticket.href) actionCell.append(actionLink("Ver detalhes", ticket.href, false));
      else actionCell.append(element("span", "demo-help", "Detalhe indisponível nesta demo"));
      row.append(actionCell);
      body.append(row);
    });
    table.append(caption, head, body);
    shell.append(table);
    return shell;
  }

  function renderDashboard(container) {
    container.append(pageHeader(
      `Olá, ${data.persona.name.split(" ")[0]}`,
      `Acompanhe os chamados demonstrativos de ${data.persona.organization}.`,
      actionLink("Abrir chamado", "/portal/demo/chamados/novo/", true),
    ));
    const metrics = element("section", "row g-3");
    metrics.setAttribute("aria-label", "Resumo dos chamados");
    data.metrics.forEach((metric) => {
      const column = element("div", "col-md-4");
      const card = element("article", `demo-card demo-metric demo-metric--${metric.tone}`);
      card.append(element("span", "", metric.label), element("strong", "", String(metric.value)));
      column.append(card);
      metrics.append(column);
    });
    container.append(metrics);
    const section = element("section", "demo-section");
    const heading = element("div", "demo-section-head");
    heading.append(element("h2", "", "Chamados recentes"), actionLink("Ver todos", "/portal/demo/chamados/", false));
    section.append(heading, ticketTable(data.tickets));
    container.append(section);
  }

  function renderTickets(container) {
    container.append(pageHeader(
      "Meus chamados",
      "Consulte prioridade, status e última atualização dos chamados demonstrativos.",
      actionLink("Abrir chamado", "/portal/demo/chamados/novo/", true),
    ));
    container.append(ticketTable(data.tickets));
  }

  function definitionItem(term, value) {
    const wrapper = element("div");
    wrapper.append(element("dt", "", term));
    const description = element("dd");
    if (value instanceof root.Node) description.append(value);
    else description.textContent = value;
    wrapper.append(description);
    return wrapper;
  }

  function timelineItem(interaction) {
    const item = element("li");
    const time = element("time", "", interaction.at);
    if (!interaction.at.includes("agora")) {
      time.dateTime = interaction.at.replace(/^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})$/, "$3-$2-$1T$4:$5:00-03:00");
    }
    item.append(time, element("strong", "", interaction.author), element("p", "", interaction.message));
    return item;
  }

  function feedback(message) {
    const alert = element("div", "alert alert-success demo-feedback", message);
    alert.setAttribute("role", "status");
    return alert;
  }

  function renderTicketDetail(container) {
    const ticket = data.featuredTicket;
    const breadcrumb = element("nav", "demo-breadcrumb");
    breadcrumb.setAttribute("aria-label", "Navegação estrutural");
    breadcrumb.append(actionLink("Meus chamados", "/portal/demo/chamados/", false), documentRef.createTextNode(` / ${ticket.number}`));
    container.append(breadcrumb, pageHeader(ticket.number, ticket.subject));
    const details = element("dl", "demo-detail-grid");
    details.append(
      definitionItem("Produto", ticket.product),
      definitionItem("Prioridade", priorityBadge(ticket.priority)),
      definitionItem("Status", statusBadge(ticket)),
      definitionItem("Criado em", ticket.createdAt),
    );
    container.append(details);
    const description = element("section", "demo-card demo-panel demo-section");
    description.append(element("h2", "", "Descrição"), element("p", "", ticket.description));
    container.append(description);
    const history = element("section", "demo-card demo-panel demo-section");
    history.append(element("h2", "", "Histórico e interações"));
    const timeline = element("ol", "demo-timeline");
    ticket.interactions.forEach((interaction) => timeline.append(timelineItem(interaction)));
    history.append(timeline);
    container.append(history);
    const response = element("section", "demo-card demo-panel demo-section");
    response.append(element("h2", "", "Responder chamado"));
    const form = element("form", "demo-form");
    const label = element("label", "form-label", "Resposta");
    label.htmlFor = "demoReply";
    const textarea = element("textarea", "form-control");
    textarea.id = "demoReply";
    textarea.name = "reply";
    textarea.required = true;
    textarea.maxLength = 1000;
    textarea.setAttribute("aria-describedby", "demoReplyHelp");
    const help = element("p", "demo-help mt-2", "A resposta será exibida somente nesta tela e não será persistida.");
    help.id = "demoReplyHelp";
    const button = element("button", "btn btn-brand", "Adicionar resposta demonstrativa");
    button.type = "submit";
    form.append(label, textarea, help, button);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      timeline.append(timelineItem({ at: "26/09/2026 agora", author: data.persona.name, message: textarea.value.trim() }));
      textarea.value = "";
      form.querySelector(".demo-feedback")?.remove();
      form.append(feedback("Resposta adicionada apenas à demonstração."));
    });
    response.append(form);
    container.append(response);
  }

  function formField(id, labelText, control) {
    const wrapper = element("div", "col-12");
    const label = element("label", "form-label", labelText);
    label.htmlFor = id;
    control.id = id;
    control.name = id;
    wrapper.append(label, control);
    return wrapper;
  }

  function selectControl(items, prompt) {
    const select = element("select", "form-select");
    select.required = true;
    const empty = element("option", "", prompt);
    empty.value = "";
    select.append(empty);
    items.forEach((item) => {
      const value = typeof item === "string" ? item : item.value;
      const label = typeof item === "string" ? item : item.label;
      const option = element("option", "", label);
      option.value = value;
      select.append(option);
    });
    return select;
  }

  function renderNewTicket(container) {
    const breadcrumb = element("nav", "demo-breadcrumb");
    breadcrumb.setAttribute("aria-label", "Navegação estrutural");
    breadcrumb.append(actionLink("Meus chamados", "/portal/demo/chamados/", false), documentRef.createTextNode(" / Abrir chamado"));
    container.append(breadcrumb, pageHeader("Abrir chamado", "Preencha os dados abaixo para simular a abertura de um chamado."));
    const panel = element("section", "demo-card demo-panel");
    const form = element("form", "demo-form row g-3");
    const product = selectControl(data.products, "Selecione um produto");
    const priority = selectControl(data.priorities, "Selecione uma prioridade");
    const subject = element("input", "form-control");
    subject.type = "text";
    subject.required = true;
    subject.maxLength = 160;
    const description = element("textarea", "form-control");
    description.required = true;
    description.maxLength = 2000;
    const attachment = element("input", "form-control");
    attachment.type = "file";
    attachment.setAttribute("aria-describedby", "demoAttachmentHelp");
    const attachmentField = formField("demoAttachment", "Anexo opcional", attachment);
    const attachmentHelp = element("p", "demo-help mt-2 mb-0", "O arquivo não será enviado, lido ou armazenado nesta demonstração.");
    attachmentHelp.id = "demoAttachmentHelp";
    attachmentField.append(attachmentHelp);
    form.append(
      formField("demoProduct", "Produto", product),
      formField("demoSubject", "Assunto", subject),
      formField("demoPriority", "Prioridade", priority),
      formField("demoDescription", "Descrição", description),
      attachmentField,
    );
    const actions = element("div", "col-12 d-flex flex-column flex-sm-row gap-2");
    const submit = element("button", "btn btn-brand", "Abrir chamado demonstrativo");
    submit.type = "submit";
    actions.append(submit, actionLink("Cancelar", "/portal/demo/dashboard/", false));
    form.append(actions);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      form.querySelector(".demo-feedback")?.remove();
      const success = feedback("Chamado demonstrativo criado com sucesso. Número fictício: KDH-DEMO-000001. Nenhum dado foi enviado ou persistido.");
      success.append(actionLink("Voltar para Meus chamados", "/portal/demo/chamados/", false));
      actions.insertAdjacentElement("afterend", success);
      form.reset();
    });
    panel.append(form);
    container.append(panel);
  }

  function init() {
    const page = documentRef.body.dataset.demoPage;
    const container = documentRef.getElementById("demoPageContent");
    if (!container) return;
    const activePage = page === "ticket-detail" ? "chamados" : page;
    documentRef.querySelector(`[data-demo-nav="${activePage}"]`)?.setAttribute("aria-current", "page");
    const renderers = { dashboard: renderDashboard, chamados: renderTickets, "ticket-detail": renderTicketDetail, "new-ticket": renderNewTicket };
    const renderer = renderers[page];
    if (renderer) renderer(container);
    else container.append(pageHeader("Página indisponível", "Esta área não faz parte da demonstração atual."));
  }

  init();
})(typeof window !== "undefined" ? window : globalThis);
