# Blog Koddahub

A fonte editorial é `docs/editorial/**/*.md`. VAL — Valor, Autoridade e
Linguagem Koddahub — prepara o rascunho, que passa por revisão e aprovação
editorial antes de receber `status: published` e `publish_date` no front matter.
Toda redação e revisão segue as
[diretrizes didáticas da VAL](editorial/diretrizes-didaticas-val.md).
VAL é identidade editorial, não pessoa física. O rascunho inaugural permanece
em `docs/editorial/rascunhos/` com `status: draft`; a imagem original está em
`docs/editorial/assets/`. Esses arquivos são versionados, mas não entram em
`dist/` nem no site público enquanto o artigo estiver em revisão.

O fluxo de autoridade é: VAL → conteúdo → UX editorial → glossário → recursos
visuais → QA → `scripts/build.py` → deploy → Kodda. Aprovação e publicação
continuam condicionadas ao escopo autorizado. O build copia
`public/` para `dist/`, renderiza a home institucional, lê os Markdown e gera
`/blog/` e `/blog/<slug>/`. O sitemap inclui apenas as URLs geradas. Não edite
`dist/` manualmente. A publicação produtiva não faz parte do build.

O status deve ser `draft`, `review`, `scheduled`, `published` ou `archived`.
`published` e `scheduled` aparecem somente quando `publish_date` chega. O status
`scheduled` permite a inclusão no build do dia programado; os demais estados
ficam fora do site. Um artigo
publicado requer `title`, `seo_title`, `meta_description`, `summary`, `category`,
`reading_time`, `slug` e `publish_date` ISO (AAAA-MM-DD). O slug deve ter
letras minúsculas, números e hífens. `cover`, `cover_alt`, `cover_width` e
`cover_height` são obrigatórios para qualquer artigo elegível ao build; a capa
deve apontar para arquivo existente em `/assets/images/`. Sem capa, o build
interrompe a publicação. `modified_date` é opcional; use apenas
quando houver alteração editorial real. Antes da publicação, escolha a
capa definitiva, otimize-a para web, coloque-a em `public/assets/images/` e
preencha `cover`, `cover_alt`, `cover_width` e `cover_height`. O alt deve
descrever a imagem efetivamente usada, não apenas o conceito do prompt. O corpo
Markdown suporta parágrafos, H2, H3, listas simples, listas numeradas, negrito
e marcadores `[[visual:id]]`. Cada marcador precisa corresponder a um item de
`didactic_visuals` no front matter, com tipo, título, legenda, alt text e
classificação dos dados. O build oferece fluxo, tabela responsiva, cards de
comparação e gráfico de barras; números fictícios devem ser marcados como
exemplo ilustrativo. Links editoriais sugeridos no rascunho não são publicados
no corpo do artigo; quando apontam para outro artigo já publicado, alimentam
a seção “Continue lendo”. Os demais links da seção são escolhidos primeiro
pela mesma categoria e depois pela data. Links futuros ou inválidos não entram
na página. Não use HTML bruto como conteúdo editorial.

A partir de 15/09/2026, **15 minutos de leitura é o padrão editorial** para
novos artigos. Escreva conteúdo que justifique esse tempo: o build exige
`reading_time: 15 minutos` e pelo menos 2.250 palavras no corpo para artigos
com `publish_date` nessa data ou posterior. Essa contagem é uma proteção mínima,
não substitui revisão de utilidade, clareza, fontes e redundância. Artigos mais
antigos preservam o tempo real indicado até uma revisão de conteúdo; não altere
apenas o rótulo. Todo artigo também precisa de capa definitiva antes de entrar
no site.

A série [#DescomplicandoATI](editorial/serie-descomplicandoati.md) começou com
um artigo sobre RPA. Ela é adicional às 30 pautas originais e segue a mesma
exigência de capa e revisão factual. Seus artigos seguem o percurso “O que é?” →
“Exemplo simples” → “Por que importa?” → “Como funciona?” → “Exemplo real” →
“O que fazer com isso?”.

A home usa `public/blog/index.template.html`; o artigo usa
`public/blog/article.template.html`; o renderizador está em `scripts/blog.py`.
O card em destaque é sempre o artigo com a data de publicação mais recente;
em caso de empate, o slug define uma ordem estável. Não há slug fixo de destaque.
O título “Outras publicações” separa o destaque da grade e aparece apenas
quando existe pelo menos mais um artigo.
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

## Publicação agendada

Os 30 textos do [planejamento editorial](editorial/planejamento-30-artigos-2026.md)
foram preparados separadamente do rascunho inaugural. Quatro textos com pautas
de 09 a 12/09 foram publicados em 12/09/2026, sua data real de publicação.
O artigo de 13/09 foi publicado com capa. Dois exemplos adicionais de n8n,
com datas editoriais retroativas de 02/09 e 03/09, foram publicados de fato
em 13/09; a data real está em `originally_published_date` no front matter.
O artigo de 14/09 também foi publicado com capa. Os 24 artigos seguintes estão
em `docs/editorial/agendados/` com `status: scheduled` e `publish_date` entre
15/09 e 08/10/2026. O texto de 15/09 já tem capa e extensão para 15 minutos;
aguarda a primeira execução à meia-noite. Os 23 posteriores ainda precisam de
capas e ampliação editorial. A trava do build impedirá a publicação até que
esses requisitos estejam completos.
Não confunda `planned_date` com a data
real: ela preserva o histórico do planejamento.

O cron do usuário `kodda` executa `scripts/publish_due.py` à 00:00 no fuso
`America/Sao_Paulo`. O script só age quando encontra artigo devido ainda ausente
em `/home/kodda/public_html/blog/`. Ele executa o build, verifica o artigo
no artefato, salva uma cópia de `blog/` e `sitemap.xml` em
`/home/kodda/site-koddahub-backups/`, atualiza apenas essas saídas e confirma
que o arquivo público existe. Em erro de cópia, restaura o backup. Se um dia
foi perdido, o script para em vez de afirmar uma data de publicação falsa;
revisar o agendamento antes de retomar. O log do cron fica em
`/home/kodda/site-koddahub-publish.log`. A publicação de conteúdo não faz push
ou commit automático.
