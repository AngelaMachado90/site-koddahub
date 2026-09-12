"""Renderiza páginas estáticas do blog a partir de Markdown editorial."""
import json
import re
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL = ROOT / "docs/editorial"
PUBLIC = ROOT / "public"


def e(value):
    return escape(str(value or ""), quote=True)


def inline(value):
    value = e(value)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)


def markdown(value):
    blocks, paragraph, items = [], [], []
    list_tag = None

    def flush():
        nonlocal list_tag
        if paragraph:
            blocks.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()
        if items:
            blocks.append(f"<{list_tag}>" + "".join("<li>" + inline(x) + "</li>" for x in items) + f"</{list_tag}>")
            items.clear()
            list_tag = None

    for raw_line in value.splitlines():
        line = raw_line.strip()
        numbered = re.match(r"[0-9]+\. (.+)", line)
        if not line:
            flush()
        elif line.startswith("## "):
            flush()
            blocks.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("### "):
            flush()
            blocks.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("- ") or numbered:
            tag = "ol" if numbered else "ul"
            if paragraph or (list_tag and list_tag != tag):
                flush()
            list_tag = tag
            items.append(numbered.group(1) if numbered else line[2:])
        elif items and raw_line.startswith(("  ", "\t")):
            items[-1] += " " + line
        elif not line.startswith("# "):
            if items:
                flush()
            paragraph.append(line)
    flush()
    return "\n".join(blocks)


def source_links(body):
    """Exibe somente URLs HTTPS presentes nas notas de referência editorial."""
    section = body.split("## Referências", 1)
    if len(section) == 1:
        return ""
    urls = []
    for match in re.findall(r"https://[^\s)]+", section[1]):
        url = match.rstrip(".,;:")
        if urlparse(url).hostname and url not in urls:
            urls.append(url)
    if not urls:
        return ""
    links = "".join(f'<li><a href="{e(url)}">{e(urlparse(url).hostname)}</a></li>' for url in urls)
    return '<section aria-labelledby="fontes-artigo"><h2 id="fontes-artigo">Fontes</h2><ul>' + links + '</ul></section>'


def articles(editorial=EDITORIAL, today=None):
    today = today or date.today()
    found = []
    for path in editorial.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", content, re.S)
        if not match:
            continue
        meta = yaml.safe_load(match[1]) or {}
        if meta.get("status") not in {"published", "scheduled"}:
            continue
        published = meta.get("publish_date")
        if not published:
            raise ValueError(f"Artigo público ou agendado sem publish_date: {path}")
        published = date.fromisoformat(str(published))
        if published > today:
            continue
        slug = str(meta.get("slug", ""))
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Slug inválido: {path}")
        for key in ("title", "seo_title", "meta_description", "summary", "category", "reading_time"):
            if not meta.get(key):
                raise ValueError(f"{key} ausente: {path}")
        meta["publish_date"] = published
        meta["body"] = match[2]
        found.append(meta)
    if len({a['slug'] for a in found}) != len(found):
        raise ValueError("Slugs duplicados")
    return sorted(found, key=lambda a: a["publish_date"], reverse=True)


def shell(home, body, title, description, canonical, site_url, version, schema, article=False):
    header = re.search(r'<header class="site-header.*?</header>', home, re.S).group()
    footer = re.search(r'<footer class="site-footer.*?</footer>', home, re.S).group()
    chat = re.search(r'<div class="kodda-chat">.*?(?=\n  <script src=)', home, re.S).group()
    scripts = re.search(r'  <script src=.*?</script>', home, re.S).group()
    header = header.replace('href="#inicio"', 'href="/"').replace('href="#servicos"', 'href="/#servicos"').replace('href="#processo"', 'href="/#processo"').replace('href="#cases"', 'href="/#cases"').replace('href="#contato"', 'href="/#contato"')
    header = header.replace('<a class="nav-link" href="/blog/">Blog</a>', '<a class="nav-link" href="/blog/" aria-current="page">Blog</a>')
    footer = footer.replace('href="#inicio"', 'href="/"')
    image = site_url + '/assets/images/hero/koddahub-hero.webp'
    og_type = 'article' if article else 'website'
    schema_json = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    head = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#0a1a2f"><meta name="koddahub-chat-webhook-url" content="{{{{CHAT_WEBHOOK_URL}}}}"><link rel="canonical" href="{e(canonical)}"><meta property="og:locale" content="pt_BR"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="KoddaHub"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{e(image)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{e(image)}"><link rel="icon" type="image/webp" href="/assets/images/logo/koddahub-logo-128.webp"><link rel="stylesheet" href="/assets/vendor/bootstrap/bootstrap.min.css?v={e(version)}"><link rel="stylesheet" href="/assets/css/koddahub-tokens.css?v={e(version)}"><link rel="stylesheet" href="/assets/css/style.css?v={e(version)}"><link rel="stylesheet" href="/assets/css/blog.css?v={e(version)}"><script type="application/ld+json">{schema_json}</script></head><body><a class="skip-link" href="#conteudo">Pular para o conteúdo</a>'''
    webhook = re.search(r'<meta name="koddahub-chat-webhook-url" content="([^"]*)">', home).group(1)
    head = head.replace('{{CHAT_WEBHOOK_URL}}', webhook)
    return head + header + '<main id="conteudo">' + body + '</main>' + footer + chat + scripts + '</body></html>'


def build_blog(dist, home, site_url, version, editorial=EDITORIAL):
    entries = articles(editorial)
    cards = []
    for item in entries:
        slug = item['slug']; url = f'/blog/{slug}/'
        cards.append(f'<div class="col-md-6 col-xl-4"><article class="card blog-card h-100"><div class="card-body d-flex flex-column"><span class="badge text-bg-light align-self-start mb-3">{e(item["category"])}</span><h3 class="h4 card-title"><a class="stretched-link" href="{url}">{e(item["title"])}</a></h3><p class="card-text">{e(item["summary"])}</p><p class="small text-muted mt-auto mb-0">{e(item["publish_date"])} · {e(item["reading_time"])}</p></div></article></div>')
    listing = ''.join(cards) if cards else '<div class="col-12"><p>Os primeiros artigos estão em preparação. Enquanto isso, conheça <a href="/#processo">como trabalhamos</a>.</p></div>'
    blog_url = site_url + '/blog/'
    blog_schema = {"@context":"https://schema.org","@type":"Blog","name":"Blog Koddahub","url":blog_url,"description":"Tecnologia aplicada a problemas reais."}
    body = (PUBLIC/'blog/index.template.html').read_text(encoding='utf-8').replace('{{ARTICLES}}', listing)
    target = dist/'blog'; target.mkdir(exist_ok=True)
    (target/'index.html').write_text(shell(home, body, 'Blog Koddahub | Tecnologia aplicada a problemas reais', 'Conteúdos sobre automação, inteligência artificial, dados, desenvolvimento, qualidade, DevOps e tecnologia aplicada ao negócio.', blog_url, site_url, version, blog_schema), encoding='utf-8')
    for item in entries:
        url = blog_url + item['slug'] + '/'
        related = '<ul>' + ''.join(f'<li><a href="/blog/{e(other["slug"])}/">{e(other["title"])}</a></li>' for other in entries if other is not item) + '</ul>' if len(entries)>1 else '<p><a href="/blog/">Ver todos os artigos</a></p>'
        content = markdown(item['body'].split('## Links internos sugeridos')[0].split('## Referências')[0].split('## Imagem de capa')[0]) + source_links(item['body'])
        cover = ''
        if item.get('cover'):
            cover_path = str(item['cover'])
            if not re.fullmatch(r'/assets/images/[a-zA-Z0-9_./-]+', cover_path) or '..' in cover_path:
                raise ValueError('Caminho de capa inválido')
            if not (PUBLIC / cover_path.lstrip('/')).is_file():
                raise ValueError('Imagem de capa inexistente')
            for key in ('cover_alt', 'cover_width', 'cover_height'):
                if not item.get(key):
                    raise ValueError(f'{key} obrigatório com cover')
            cover = f'<img class="blog-cover rounded my-4" src="{e(cover_path)}" width="{e(item["cover_width"])}" height="{e(item["cover_height"])}" alt="{e(item["cover_alt"])}">'
        body = (PUBLIC/'blog/article.template.html').read_text(encoding='utf-8')
        for key, value in {'CATEGORY':e(item['category']),'TITLE':e(item['title']),'SUMMARY':e(item['summary']),'DATE':e(item['publish_date']),'READING_TIME':e(item['reading_time']),'AUTHOR':e(item.get('author','VAL — Valor, Autoridade e Linguagem Koddahub')),'COVER':cover,'CONTENT':content,'RELATED':related}.items():
            body = body.replace('{{'+key+'}}', value)
        schema = {"@context":"https://schema.org","@type":"BlogPosting","headline":item['title'],"description":item['meta_description'],"datePublished":str(item['publish_date']),"author":{"@type":"Organization","name":"Koddahub"},"mainEntityOfPage":url}
        if item.get('modified_date'):
            schema['dateModified'] = str(item['modified_date'])
        page = shell(home, body, item['seo_title'], item['meta_description'], url, site_url, version, schema, True)
        target_dir = target/item['slug']; target_dir.mkdir(exist_ok=True)
        (target_dir/'index.html').write_text(page, encoding='utf-8')
    return [blog_url] + [blog_url + item['slug'] + '/' for item in entries]
