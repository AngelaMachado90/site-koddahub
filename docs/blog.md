# Blog Koddahub

A fonte editorial é `docs/editorial/**/*.md`. VAL — Valor, Autoridade e
Linguagem Koddahub — prepara o rascunho, que passa por revisão e aprovação
editorial antes de receber `status: published` e `publish_date` no front matter.
VAL é identidade editorial, não pessoa física. O rascunho inaugural permanece
em `docs/editorial/rascunhos/` com `status: draft` e não entra no site.

O fluxo é: VAL → Markdown editorial → aprovação → `scripts/build.py` →
`dist/blog/` → validação local → publicação em etapa separada. O build copia
`public/` para `dist/`, renderiza a home institucional, lê os Markdown e gera
`/blog/` e `/blog/<slug>/`. O sitemap inclui apenas as URLs geradas. Não edite
`dist/` manualmente. A publicação produtiva não faz parte do build.

O status deve ser `draft`, `review`, `scheduled`, `published` ou `archived`.
Somente `published` com `publish_date` até a data do build aparece. Um artigo
publicado requer `title`, `seo_title`, `meta_description`, `summary`, `category`,
`reading_time`, `slug` e `publish_date` ISO (AAAA-MM-DD). O slug deve ter
letras minúsculas, números e hífens. `cover`, `cover_alt`, `cover_width` e `cover_height` são opcionais em conjunto; a capa deve apontar para arquivo existente em `/assets/images/`. `modified_date` é opcional; use apenas
quando houver alteração editorial real. O corpo Markdown suporta parágrafos,
H2, H3, listas simples e negrito. Links editoriais sugeridos no rascunho não
são publicados automaticamente. Não use HTML bruto como conteúdo editorial.

A home usa `public/blog/index.template.html`; o artigo usa
`public/blog/article.template.html`; o renderizador está em `scripts/blog.py`.
O cabeçalho, rodapé e chatbot são derivados do template institucional durante
o build. O CSS complementar está em `public/assets/css/blog.css`; Bootstrap
5.3 continua a base do grid e dos componentes.

Cada página tem title, description, canonical, Open Graph, Twitter card e
JSON-LD. A home usa `Blog`; artigos usam `BlogPosting` com data verdadeira.
A canonical de listagem é `/blog/`. Diretórios com `index.html` recebem a barra
final do servidor HTTP/Apache. Não há rewrite que transforme 404 em 200.

Para validar: `python3 -m unittest discover -s tests -v`,
`python3 scripts/build.py` e sirva `dist/` com `python3 -m http.server 8000 -d dist`.
Verifique `/`, `/blog`, `/blog/`, artigo publicado e uma URL inexistente.
