# Koddahub — Site Institucional

Site institucional da Koddahub, desenvolvido como aplicação web estática com build automatizado, Bootstrap 5.3 e estrutura editorial para o Blog Koddahub.

- [Site](https://koddahub.com.br)
- [Blog](https://koddahub.com.br/blog/)
- [Repositório](https://github.com/AngelaMachado90/site-koddahub)

## Visão geral

A página institucional apresenta soluções, processo de trabalho, cases e contato em seções da rota `/`. O projeto também inclui o Blog Koddahub, um launcher de chatbot, metadados de SEO, assets locais e documentação editorial. Não há páginas individuais de soluções no código atual.

`public/` contém os templates e assets editáveis; `docs/editorial/` contém a fonte dos artigos. `scripts/build.py` combina essas entradas em `dist/`, que é o artefato para servir. **Não edite nem publique `public/` diretamente; não edite `dist/` manualmente.**

## Stack

HTML5, CSS3, JavaScript sem framework de aplicação, Python 3 com PyYAML e Bootstrap 5.3.8 distribuído em `public/assets/vendor/bootstrap/`. A produção usa Apache com `DocumentRoot` em `/home/kodda/public_html`.

## Estrutura do projeto

```text
site-koddahub/
├── public/
│   ├── index.template.html       # página institucional
│   ├── blog/                     # templates de listagem e artigo
│   └── assets/                   # CSS, JavaScript, imagens e Bootstrap local
├── scripts/
│   ├── build.py                  # build do site e sitemap
│   └── blog.py                   # seleção e renderização dos artigos
├── docs/
│   ├── blog.md                   # fluxo editorial e arquitetura do blog
│   ├── design-system/README.md
│   └── editorial/               # Markdown editorial, quando houver textos
├── tests/test_blog.py
├── deploy/apache/               # configuração versionada do staging HTTP
├── dist/                        # saída gerada, ignorada pelo Git
└── README.md
```

## Arquitetura

```text
public/ + docs/editorial/
          ↓
   scripts/build.py
          ↓
        dist/
          ↓
validação local → staging quando disponível → produção autorizada
```

O build copia os arquivos de `public/` para `dist/`, exclui os templates da cópia, renderiza `index.html`, gera `/blog/` e artigos elegíveis, e atualiza `sitemap.xml` e `version.txt`. Ele recria `dist/` a cada execução. Staging possui diretório e VirtualHost HTTP configurados, mas `staging.koddahub.com.br` não resolvia por DNS na última verificação; portanto a validação pública por HTTPS ainda é pendente.

## Desenvolvimento local

Pré-requisitos: Git, Python 3 e o módulo Python `yaml` (PyYAML). Não há `package.json`, Dockerfile nem gerenciador de dependências versionado neste repositório. Confirme a dependência com `python3 -c 'import yaml'` antes do build.

```bash
git clone https://github.com/AngelaMachado90/site-koddahub.git
cd site-koddahub
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

Abra `http://localhost:8000/` e `http://localhost:8000/blog/`. O servidor Python serve diretórios com `index.html` e preserva 404 para rotas inexistentes; ele é apenas para preview local.

## Build

```bash
python3 scripts/build.py
```

Por padrão, `SITE_URL` é `https://koddahub.com.br`, `CHAT_WEBHOOK_URL` fica vazio e `ASSET_VERSION` usa o horário do build. URLs configuradas precisam ser HTTP(S) válidas. Um artigo `published` sem metadados obrigatórios, data válida ou slug válido interrompe o build com erro; não publique o artefato após uma falha. Confira `dist/index.html`, `dist/blog/index.html` e `dist/sitemap.xml` antes de qualquer deploy.

## Blog Koddahub

VAL prepara o Markdown editorial → revisão e aprovação → `status: published` com `publish_date` → build → `/blog/` e `/blog/<slug>/`. A fonte é `docs/editorial/**/*.md`; `scripts/blog.py` seleciona os textos e gera os HTMLs. Os estados previstos no fluxo editorial são `draft`, `review`, `scheduled`, `published` e `archived`. O build inclui `published` e `scheduled` somente quando `publish_date` chega; o agendamento depende de execução diária do build e deploy do blog. O rascunho inaugural fica em `docs/editorial/rascunhos/`, com status `draft`; sua imagem de referência fica em `docs/editorial/assets/`. Nenhum dos dois entra no site público enquanto estiver em revisão.

### VAL — Valor, Autoridade e Linguagem Koddahub

VAL é a identidade editorial usada na preparação dos conteúdos do blog, não uma pessoa humana. Metadados, templates, limites do Markdown e regras de publicação estão em [Arquitetura do Blog](docs/blog.md).

## Rotas

| Rota | Conteúdo |
| --- | --- |
| `/` | Página institucional; soluções, processo, cases e contato são âncoras desta página. |
| `/blog/` | Listagem de artigos publicados; exibe estado vazio quando não há artigos. |
| `/blog/<slug>/` | Artigo gerado apenas quando elegível para publicação. |

Em Apache, `/blog` redireciona para `/blog/` por se tratar de um diretório com `index.html`. Rotas inexistentes devem continuar retornando 404.

## SEO

A home e as páginas do blog têm title, meta description, canonical, Open Graph e metadados para Twitter/X. O blog também gera JSON-LD `Blog` e `BlogPosting`; o sitemap é montado no build somente com URLs geradas. A canonical da listagem é `/blog/`. Confira metadados e links após cada publicação de artigo.

## Chatbot e configuração

O launcher flutuante e sua lógica ficam em `public/index.template.html` e `public/assets/js/site.js`; o blog reutiliza o mesmo shell no build. O JavaScript lê o endpoint da meta tag preenchida por `CHAT_WEBHOOK_URL` durante o build. **Status atual: integração de webhook pendente** nos artefatos verificados de staging e produção; o launcher aparece, mas o envio de mensagens não está configurado.

| Variável | Uso |
| --- | --- |
| `SITE_URL` | Origem usada em canonical, Open Graph e sitemap; padrão `https://koddahub.com.br`. |
| `CHAT_WEBHOOK_URL` | Endpoint público do chat injetado no HTML; padrão vazio. |
| `ASSET_VERSION` | Versão nas URLs de CSS/JS e em `version.txt`; padrão: horário do build. |

A URL do webhook fica visível no navegador: não inclua tokens ou segredos nela. Configure validação, CORS e limites de requisições no backend antes de habilitar o envio.

## Design System

Novas interfaces devem reutilizar o Bootstrap 5.3 local, os tokens em `public/assets/css/koddahub-tokens.css` e os componentes/CTAs existentes. Consulte o [Design System](docs/design-system/README.md) para detalhes da identidade visual.

## Validação

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build.py
git diff --check
```

Depois do build, valide `/`, `/blog/`, `/blog` (redirecionamento) e uma URL inexistente (404) no preview. Os testes em `tests/test_blog.py` verificam exclusão de rascunho, elegibilidade por data, geração de artigo e metadados. Eles não substituem revisão visual mobile, links e teste do chatbot com endpoint configurado.

## Deploy

A publicação agendada do blog roda às 09:00 no fuso `America/Sao_Paulo` pelo cron do usuário `kodda`. `scripts/publish_due.py` detecta artigos devidos, executa o build, guarda backup de `blog/` e `sitemap.xml`, copia apenas esses artefatos e verifica as páginas novas. Se uma data passou sem publicação, o job interrompe para revisão da data real; consulte o log local e a seção de agendamento em [docs/blog.md](docs/blog.md).


O fluxo é fonte → commit → build → validação → staging quando disponível → produção autorizada. Publica-se **somente o conteúdo de `dist/`**, nunca a árvore `public/`, documentação, `.git` ou arquivos de ambiente. O destino produtivo confirmado é `/home/kodda/public_html`, servido por Apache. O staging usa `/home/kodda/staging/site-koddahub` e o VirtualHost em `deploy/apache/staging.koddahub.com.br.conf`; DNS/HTTPS públicos ainda precisam ser concluídos antes de tratá-lo como etapa de homologação externa.

Antes de atualizar produção, preserve uma cópia íntegra da versão servida e defina como restaurá-la se a validação falhar. Não existe script de rollback versionado. Após publicar, verifique HTTP, conteúdo, assets, canonical, sitemap e 404 no domínio público. Não faça deploy ou push como efeito colateral do build.

Checklist de publicação:

- [ ] Estado do Git e alterações locais revisados; documentação atualizada.
- [ ] Testes e build aprovados; artefato `dist/` conferido.
- [ ] Home, blog, links, mobile e SEO básico validados.
- [ ] Cópia para rollback disponível e produção autorizada.
- [ ] Rotas e assets verificados após a publicação.

## Git, contribuição e segurança

Edite a fonte, valide, documente, gere o build, faça staging seletivo e commit com mensagem clara; passe por revisão antes de deploy autorizado. `dist/` é ignorado pelo Git. Nunca versione `.env`, senhas, tokens, chaves privadas, access tokens ou segredos de webhook. O `.gitignore` cobre `.env`, `dist/` e `__pycache__/`; revise outros arquivos sensíveis antes do staging.

## Documentação complementar

- [Arquitetura e fluxo editorial do Blog](docs/blog.md)
- [Design System](docs/design-system/README.md)

## Koddahub

A Koddahub trabalha com tecnologia aplicada a problemas reais, conectando desenvolvimento, automação, dados, qualidade e inteligência a necessidades de negócio.
