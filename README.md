# KoddaHub

Site institucional da KoddaHub.

## Desenvolvimento

```bash
python3 scripts/build.py
```

O código editável fica em `public/`. O resultado público é gerado em `dist/` e não deve ser editado manualmente.

## Design System

A identidade visual, os tokens e os componentes da marca estão documentados no
[Koddahub Design System](docs/design-system/README.md). Os tokens em
`public/assets/css/koddahub-tokens.css` são a fonte de verdade da interface.

## Chatbot

O launcher do chatbot fica no canto inferior direito e usa a identidade do
Design System. O botão circular mede 64 × 64 px no desktop e 56 × 56 px no
mobile. O texto “Tire suas dúvidas” aparece como tooltip em hover ou foco; o
nome acessível permanece disponível por `aria-label`.

A lógica de abertura e mensagens está em `public/assets/js/site.js`. O endpoint
é injetado no HTML durante o build pela variável `CHAT_WEBHOOK_URL`. A URL será
visível no navegador e não pode conter tokens ou credenciais. Sem a variável, o
launcher visual pode ser validado, mas o envio não é considerado funcional.

Cada ambiente deve usar seu próprio endpoint:

```bash
SITE_URL=https://staging.koddahub.com.br \
CHAT_WEBHOOK_URL=https://endpoint-de-teste.example/webhook \
python3 scripts/build.py
```

O webhook deve aceitar apenas `POST`, validar e limitar payloads, configurar
CORS para a origem esperada, aplicar rate limiting e devolver JSON com uma
string em `output` ou `message`. Esses controles pertencem ao servidor/n8n, não
ao JavaScript público.

## Publicação

O fluxo oficial separa os ambientes:

```text
SOURCE /home/kodda/projects/site-koddahub
  -> BUILD /home/kodda/projects/site-koddahub/dist
  -> STAGING /home/kodda/staging/site-koddahub
  -> VALIDACAO https://staging.koddahub.com.br
  -> PRODUCTION /home/kodda/public_html
```

O staging usa o VirtualHost versionado em
`deploy/apache/staging.koddahub.com.br.conf`. O artefato publicado deve conter
somente o conteúdo de `dist/`. Nunca copie `.git`, `.env`, documentação, scripts
de desenvolvimento, segredos ou credenciais.

Enquanto o DNS não estiver criado, valide o VirtualHost localmente com o header
`Host`. Depois que o DNS apontar para o servidor, emita o certificado pelo mesmo
mecanismo Let's Encrypt já usado no servidor e só então valide HTTPS. Produção
não deve ser usada como staging e exige uma etapa independente, aprovação e
plano de rollback.

## Blog

O build gera `dist/blog/index.html` e uma pasta `dist/blog/<slug>/index.html`
por artigo publicado. A fonte editorial única é `docs/editorial/**/*.md`, com
front matter YAML e corpo Markdown. Consulte [o fluxo do blog](docs/blog.md)
para status, metadados, URLs e publicação. O build requer PyYAML no Python local.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```
