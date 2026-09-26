const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  try {
    await page.goto("http://127.0.0.1:8000/portal/demo/chamados/", { waitUntil: "networkidle" });
    await page.getByText("Nenhum chamado encontrado.").waitFor();
    await page.goto("http://127.0.0.1:8000/portal/demo/chamados/novo/", { waitUntil: "networkidle" });
    await page.locator("select").nth(0).selectOption({ index: 1 });
    await page.locator("form input:not([type='file'])").fill("Chamado E2E HML");
    await page.locator("select").nth(1).selectOption("p3");
    await page.locator("textarea").fill("Mensagem inicial persistida pelo E2E HML.");
    await page.getByRole("button", { name: "Abrir chamado" }).click();
    await page.getByText(/Chamado KDH-\d{4}-\d{6} criado\./).waitFor();
    await page.getByRole("link", { name: "Abrir", exact: true }).click();
    await page.getByText("Mensagem inicial persistida pelo E2E HML.").waitFor();
    await page.getByText("created", { exact: true }).waitFor();
    await page.locator("textarea").fill("Resposta persistida pelo E2E HML.");
    await page.getByRole("button", { name: "Enviar resposta" }).click();
    await page.getByText("Resposta persistida pelo E2E HML.").waitFor();
    await page.reload({ waitUntil: "networkidle" });
    await page.getByText("Mensagem inicial persistida pelo E2E HML.").waitFor();
    await page.getByText("Resposta persistida pelo E2E HML.").waitFor();
    console.log("E2E HML: fluxo persistente validado");
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
