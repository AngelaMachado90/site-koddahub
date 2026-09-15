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
GA4_MEASUREMENT_ID = "G-3DNTXV2CYK"


def google_tag():
    return f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{GA4_MEASUREMENT_ID}');</script>'''


def e(value):
    return escape(str(value or ""), quote=True)


def inline(value):
    value = e(value)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)


def didactic_visual_html(item):
    """Renderiza um recurso didático declarado no front matter editorial."""
    visual_type = item.get("type")
    title = e(item.get("title"))
    caption = e(item.get("caption"))
    alt = e(item.get("alt"))
    data_kind = str(item.get("data_kind", "NÃO SE APLICA")).upper()
    label = f'<span class="blog-visual-data">{e(data_kind)}</span>' if data_kind != "NÃO SE APLICA" else ""

    if visual_type in {"flow", "pipeline", "steps"}:
        flow_nodes = []
        for index, node in enumerate(item.get("items", []), 1):
            number = f'<span class="blog-step-number">{e(index)}</span>' if visual_type == "steps" else ''
            flow_nodes.append(f'<div class="blog-flow-node">{number}<strong>{e(node["label"])}</strong><span>{e(node.get("detail"))}</span></div>')
        nodes = '<span class="blog-flow-arrow" aria-hidden="true">↓</span>'.join(flow_nodes)
        warning = f'<p class="blog-flow-warning"><strong>{e(item["warning_title"])}</strong> {e(item["warning_text"])}</p>' if item.get('warning_title') else ''
        content = f'<div class="blog-flow blog-flow--{e(visual_type)}" role="img" aria-label="{alt}">{nodes}</div>{warning}'
    elif visual_type == "table":
        headers = item.get("headers", [])
        head = ''.join(f'<th scope="col">{e(value)}</th>' for value in headers)
        rows = ''.join('<tr>' + ''.join(
            f'<th scope="row">{e(value)}</th>' if index == 0 else f'<td data-label="{e(headers[index])}">{e(value)}</td>'
            for index, value in enumerate(row)
        ) + '</tr>' for row in item.get("rows", []))
        columns = ''.join('<col>' for _ in headers)
        content = f'<div class="blog-comparison"><table class="table blog-comparison__table"><colgroup>{columns}</colgroup><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    elif visual_type in {"comparison", "cards", "numbered_grid", "checklist"}:
        card_items = []
        for index, card in enumerate(item.get("items", []), 1):
            number = f'<span class="blog-card-number">{e(index)}</span>' if visual_type == "numbered_grid" else ''
            marker = '<span class="blog-card-x" aria-hidden="true">×</span>' if visual_type == "checklist" else ''
            card_items.append(f'<div class="blog-concept-card">{number}{marker}<h3>{e(card["title"])}</h3><p>{e(card["text"])}</p></div>')
        cards = ''.join(card_items)
        content = f'<div class="blog-concept-grid" role="group" aria-label="{alt}">{cards}</div>'
    elif visual_type == "bar_chart":
        values = [float(bar.get("value", 0)) for bar in item.get("items", [])]
        maximum = max(values, default=1) or 1
        bars = ''.join(f'<div class="blog-bar-item"><span class="blog-bar-value">{e(bar.get("value"))}</span><span class="blog-bar" style="--bar-size:{max(0, float(bar.get("value", 0))) / maximum * 100:.2f}%"></span><span class="blog-bar-name">{e(bar.get("label"))}</span></div>' for bar in item.get("items", []))
        content = f'<div class="blog-bar-chart" role="img" aria-label="{alt}">{bars}</div>'
    elif visual_type == "timeline_compare":
        timelines = ''.join(f'<div class="blog-timeline blog-timeline--{e(period.get("status"))}"><span class="blog-timeline-status">{e(period.get("status_label"))}</span><h3>{e(period["title"])}</h3><div class="blog-timeline-track" aria-hidden="true"><span style="--timeline-size:{e(period.get("size", 100))}%"></span></div><p>{e(period["text"])}</p></div>' for period in item.get('items', []))
        content = f'<div class="blog-timeline-grid" role="img" aria-label="{alt}">{timelines}</div>'
    elif visual_type == "dot_plot":
        values = [float(value) for value in item.get('values', [])]
        maximum = max(values, default=1) or 1
        dots = ''.join(f'<span class="blog-dot" style="--dot-position:{value / maximum * 100:.2f}%"><span>{e(format(value, "g"))}</span></span>' for value in values)
        summaries = ''.join(f'<div><span>{e(summary["label"])}</span><strong>{e(summary["value"])}</strong></div>' for summary in item.get('summaries', []))
        content = f'<div class="blog-dot-plot" role="img" aria-label="{alt}"><div class="blog-dot-axis">{dots}</div><div class="blog-stat-grid">{summaries}</div></div>'
    elif visual_type == "dashboard":
        details = ''.join(f'<div class="blog-dashboard-detail"><span>{e(detail["label"])}</span><strong>{e(detail["value"])}</strong></div>' for detail in item.get('details', []))
        content = f'<div class="blog-dashboard" role="img" aria-label="{alt}"><div class="blog-dashboard-kpi"><span>{e(item.get("kpi_label"))}</span><strong>{e(item.get("kpi_value"))}</strong><small>{e(item.get("kpi_change"))}</small></div><div class="blog-dashboard-trend"><span>Tendência</span><svg viewBox="0 0 320 80" aria-hidden="true" focusable="false"><polyline points="0,65 55,56 110,60 165,38 220,42 270,20 320,12"/></svg></div><div class="blog-dashboard-grid">{details}</div><p class="blog-dashboard-updated">Atualizado: {e(item.get("updated"))}</p></div>'
    else:
        raise ValueError(f"Tipo de recurso didático inválido: {visual_type}")
    return f'<figure class="blog-visual blog-visual--{e(visual_type)}"><div class="blog-visual-heading"><h2>{title}</h2>{label}</div>{content}<figcaption>{caption}</figcaption></figure>'


def markdown(value, components=None):
    components = components or {}
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
        elif re.fullmatch(r"\[\[visual:[a-z0-9-]+\]\]", line):
            flush()
            visual_id = line[9:-2]
            if visual_id not in components:
                raise ValueError(f"Recurso didático não declarado: {visual_id}")
            blocks.append(components[visual_id])
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


def glossary_html(items):
    if not items:
        return ''
    cards = []
    for index, item in enumerate(items):
        panel = f'glossary-definition-{index}'
        cards.append(f'''<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{panel}" aria-expanded="false" aria-controls="{panel}">{e(item['term'])}</button></h3><div id="{panel}" class="accordion-collapse collapse"><div class="accordion-body"><p>{e(item['definition'])}</p><p class="mb-3"><strong>Exemplo:</strong> {e(item['example'])}</p><button class="btn btn-sm btn-outline-primary glossary-ask-kodda" type="button" data-glossary-term="{e(item['term'])}">Perguntar ao Kodda</button></div></div></div>''')
    return '<section class="blog-glossary" aria-labelledby="glossary-title"><p class="blog-overline mb-2">Consulta rápida</p><h2 id="glossary-title">Glossário rápido</h2><div class="accordion" id="articleGlossary">' + ''.join(cards) + '</div></section>'


def page_context_html(item, entries):
    general, seen = [], set()
    for entry in entries:
        for glossary_item in entry.get('glossary') or []:
            key = glossary_item['term'].casefold()
            if key not in seen:
                seen.add(key)
                general.append(glossary_item)
    context = {'page_type': 'blog', 'article_slug': item['slug'], 'article_title': item['title'], 'article_category': item['category'], 'article_summary': item['summary'], 'glossary': item.get('glossary') or [], 'didactic_visuals': item.get('didactic_visuals') or [], 'blog_glossary': general}
    payload = json.dumps(context, ensure_ascii=False).replace('<', '\\u003c')
    return f'<script type="application/json" id="kodda-page-context">{payload}</script>'


def blog_context_html(entries):
    general, seen = [], set()
    for entry in entries:
        for item in entry.get('glossary') or []:
            key = item['term'].casefold()
            if key not in seen:
                seen.add(key)
                general.append(item)
    payload = json.dumps({'page_type': 'blog_index', 'blog_glossary': general}, ensure_ascii=False).replace('<', '\\u003c')
    return f'<script type="application/json" id="kodda-page-context">{payload}</script>'


def related_articles(item, entries, limit=3):
    """Prioriza links editoriais publicados; completa com temas próximos."""
    by_slug = {entry['slug']: entry for entry in entries if entry is not item}
    notes = item['body'].split('## Links internos sugeridos', 1)
    selected = []
    if len(notes) == 2:
        for slug in re.findall(r'^- /blog/([a-z0-9-]+)/\s*$', notes[1], re.M):
            if slug in by_slug and by_slug[slug] not in selected:
                selected.append(by_slug[slug])
    candidates = sorted(by_slug.values(), key=lambda entry: (entry['category'] != item['category'], -entry['publish_date'].toordinal(), entry['slug']))
    for candidate in candidates:
        if len(selected) >= limit:
            break
        if candidate not in selected:
            selected.append(candidate)
    return selected[:limit]


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
        for glossary_item in meta.get('glossary') or []:
            for key in ('term', 'definition', 'example', 'application'):
                if not glossary_item.get(key):
                    raise ValueError(f"Glossário sem {key}: {path}")
        visuals = meta.get('didactic_visuals') or []
        visual_ids = set()
        for visual in visuals:
            for key in ('id', 'type', 'title', 'caption', 'alt', 'data_kind'):
                if not visual.get(key):
                    raise ValueError(f"Recurso didático sem {key}: {path}")
            if visual['id'] in visual_ids:
                raise ValueError(f"ID de recurso didático duplicado: {path}")
            visual_ids.add(visual['id'])
        referenced_visuals = set(re.findall(r'\[\[visual:([a-z0-9-]+)\]\]', match[2]))
        if referenced_visuals != visual_ids:
            raise ValueError(f"Recursos didáticos declarados e usados não coincidem: {path}")
        if published >= date(2026, 9, 15):
            if meta['reading_time'] != '15 minutos' or len(match[2].split()) < 2250:
                raise ValueError(f"Artigo fora do padrão de 15 minutos (mínimo de 2250 palavras): {path}")
        meta["publish_date"] = published
        meta["body"] = match[2]
        found.append(meta)
    if len({a['slug'] for a in found}) != len(found):
        raise ValueError("Slugs duplicados")
    return sorted(found, key=lambda a: (a["publish_date"], a["slug"]), reverse=True)


def shell(home, body, title, description, canonical, site_url, version, schema, article=False, image_path=None):
    header = re.search(r'<header class="site-header.*?</header>', home, re.S).group()
    footer = re.search(r'<footer class="site-footer.*?</footer>', home, re.S).group()
    chat_match = re.search(r'<div class="kodda-chat">.*?(?=\n  <script src=)', home, re.S)
    chat = chat_match.group()
    scripts = ''.join(re.findall(r'<script\b[^>]*\bsrc="[^"]+"[^>]*></script>', home[chat_match.end():]))
    header = header.replace('href="#inicio"', 'href="/"').replace('href="#servicos"', 'href="/#servicos"').replace('href="#processo"', 'href="/#processo"').replace('href="#cases"', 'href="/#cases"').replace('href="#contato"', 'href="/#contato"')
    header = header.replace('<a class="nav-link" href="/blog/">Blog</a>', '<a class="nav-link" href="/blog/" aria-current="page">Blog</a>')
    footer = footer.replace('href="#inicio"', 'href="/"')
    image = site_url + (image_path or '/assets/images/hero/koddahub-hero.webp')
    og_type = 'article' if article else 'website'
    schema_json = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    head = f'''<!doctype html><html lang="pt-BR"><head>{google_tag()}<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#0a1a2f"><meta name="koddahub-chat-webhook-url" content="{{{{CHAT_WEBHOOK_URL}}}}"><link rel="canonical" href="{e(canonical)}"><meta property="og:locale" content="pt_BR"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="KoddaHub"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{e(image)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{e(image)}"><link rel="icon" type="image/webp" href="/assets/images/logo/koddahub-logo-128.webp"><link rel="stylesheet" href="/assets/vendor/bootstrap/bootstrap.min.css?v={e(version)}"><link rel="stylesheet" href="/assets/css/koddahub-tokens.css?v={e(version)}"><link rel="stylesheet" href="/assets/css/style.css?v={e(version)}"><link rel="stylesheet" href="/assets/css/blog.css?v={e(version)}"><script type="application/ld+json">{schema_json}</script></head><body><a class="skip-link" href="#conteudo">Pular para o conteúdo</a>'''
    webhook = re.search(r'<meta name="koddahub-chat-webhook-url" content="([^"]*)">', home).group(1)
    head = head.replace('{{CHAT_WEBHOOK_URL}}', webhook)
    return head + header + '<main id="conteudo">' + body + '</main>' + footer + chat + scripts + '</body></html>'


MONTHS_PT = ("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")


def format_date_pt(value):
    return f"{value.day} de {MONTHS_PT[value.month - 1]} de {value.year}"


def card_html(item, featured=False, position=1):
    title = e(item["title"])
    url = f'/blog/{e(item["slug"])}/'
    date_label = e(format_date_pt(item["publish_date"]))
    category = e(item["category"])
    summary = e(item["summary"])
    meta = f'<div class="blog-card-meta"><time datetime="{e(item["publish_date"])}">{date_label}</time><span aria-hidden="true">·</span><span>{e(item["reading_time"])} de leitura</span></div>'
    cover = item.get("cover")
    cover_image = ''
    if cover:
        cover_image = f'<img class="blog-card-cover" src="{e(cover)}" width="{e(item.get("cover_width", ""))}" height="{e(item.get("cover_height", ""))}" alt="" loading="lazy" decoding="async">'
    if featured:
        art_class = "blog-featured-art blog-featured-art--cover h-100" if cover_image else "blog-featured-art h-100"
        art_column_class = "col-lg-5" if cover_image else "col-lg-5 d-none d-lg-block"
        return f'''<article class="card blog-card blog-featured"><a class="blog-card-link" href="{url}" aria-label="Ler artigo: {title}"><div class="row g-0"><div class="col-lg-7"><div class="blog-card-body"><span class="blog-featured-label">Em destaque</span><span class="blog-category">{category}</span><h3 class="blog-card-title">{title}</h3><p class="blog-card-summary">{summary}</p>{meta}<span class="blog-read-link">Ler artigo <span aria-hidden="true">→</span></span></div></div><div class="{art_column_class}"><div class="{art_class}" aria-hidden="true">{cover_image}</div></div></div></a></article>'''
    tone = position % 3
    media = f'<div class="blog-card-media blog-card-media--cover" aria-hidden="true">{cover_image}</div>' if cover_image else f'<div class="blog-card-media blog-tone-{tone}" aria-hidden="true"><span>{position:02d}</span></div>'
    return f'''<div class="col-md-6 col-xl-4"><article class="card blog-card h-100"><a class="blog-card-link d-flex flex-column h-100" href="{url}" aria-label="Ler artigo: {title}">{media}<div class="blog-card-body d-flex flex-column flex-grow-1"><span class="blog-category">{category}</span><h3 class="blog-card-title">{title}</h3><p class="blog-card-summary">{summary}</p><div class="mt-auto">{meta}<span class="blog-read-link">Ler artigo <span aria-hidden="true">→</span></span></div></div></a></article></div>'''


def build_blog(dist, home, site_url, version, editorial=EDITORIAL):
    entries = articles(editorial)
    for item in entries:
        cover_path = str(item.get('cover') or '')
        if not cover_path:
            raise ValueError(f"Artigo sem capa não pode ser publicado: {item['slug']}")
        if not re.fullmatch(r'/assets/images/[a-zA-Z0-9_./-]+', cover_path) or '..' in cover_path:
            raise ValueError(f"Caminho de capa inválido: {item['slug']}")
        if not (PUBLIC / cover_path.lstrip('/')).is_file():
            raise ValueError(f"Imagem de capa inexistente: {item['slug']}")
        for key in ('cover_alt', 'cover_width', 'cover_height'):
            if not item.get(key):
                raise ValueError(f"{key} obrigatório com cover: {item['slug']}")
    featured_item = entries[0] if entries else None
    featured = card_html(featured_item, featured=True) if featured_item else ""
    remaining = [item for item in entries if item is not featured_item]
    more_heading = '<div class="blog-more-heading"><h2 id="blog-more-title">Outras publicações</h2></div>' if remaining else ''
    listing = ''.join(card_html(item, position=position) for position, item in enumerate(remaining, start=2)) if entries else '<div class="col-12"><div class="blog-empty"><p class="mb-2">Os primeiros artigos estão em preparação.</p><a href="/#processo">Conheça como trabalhamos <span aria-hidden="true">→</span></a></div></div>'
    count = f"{len(entries)} artigo{'s' if len(entries) != 1 else ''} publicado{'s' if len(entries) != 1 else ''}" if entries else "Novos textos em preparação"
    blog_url = site_url + '/blog/'
    blog_schema = {"@context":"https://schema.org","@type":"Blog","name":"Blog Koddahub","url":blog_url,"description":"Tecnologia aplicada a problemas reais."}
    body = (PUBLIC/'blog/index.template.html').read_text(encoding='utf-8').replace('{{ARTICLES}}', listing).replace('{{FEATURED}}', featured).replace('{{MORE_HEADING}}', more_heading).replace('{{COUNT}}', e(count)).replace('{{SECTION_TITLE}}', 'Artigos' if entries else 'Em breve').replace('{{PAGE_CONTEXT}}', blog_context_html(entries))
    target = dist/'blog'; target.mkdir(exist_ok=True)
    (target/'index.html').write_text(shell(home, body, 'Blog Koddahub | Tecnologia aplicada a problemas reais', 'Conteúdos sobre automação, inteligência artificial, dados, desenvolvimento, qualidade, DevOps e tecnologia aplicada ao negócio.', blog_url, site_url, version, blog_schema), encoding='utf-8')
    for item in entries:
        url = blog_url + item['slug'] + '/'
        other_articles = related_articles(item, entries)
        related = '<ul class="blog-related-list">' + ''.join(f'<li><a href="/blog/{e(other["slug"])}/">{e(other["title"])} <span aria-hidden="true">→</span></a></li>' for other in other_articles) + '</ul>' if other_articles else '<p><a href="/blog/">Ver todos os artigos</a></p>'
        components = {visual['id']: didactic_visual_html(visual) for visual in item.get('didactic_visuals') or []}
        content = markdown(item['body'].split('## Links internos sugeridos')[0].split('## Referências')[0].split('## Imagem de capa')[0], components) + source_links(item['body'])
        cover_path = str(item['cover'])
        cover = f'<img class="blog-cover rounded my-4" src="{e(cover_path)}" width="{e(item["cover_width"])}" height="{e(item["cover_height"])}" alt="{e(item["cover_alt"])}">'
        body = (PUBLIC/'blog/article.template.html').read_text(encoding='utf-8')
        cta_url = str(item.get('cta_url', '/#processo'))
        is_whatsapp = urlparse(cta_url).hostname == 'wa.me'
        cta_icon = '<svg class="icon" aria-hidden="true"><use href="/assets/images/icons/icons.svg#whatsapp"></use></svg>' if is_whatsapp else ''
        for key, value in {'CATEGORY':e(item['category']),'TITLE':e(item['title']),'SUMMARY':e(item['summary']),'DATE':e(format_date_pt(item['publish_date'])),'DATE_ISO':e(item['publish_date']),'READING_TIME':e(item['reading_time']),'AUTHOR':e(item.get('author','VAL — Valor, Autoridade e Linguagem Koddahub')),'COVER':cover,'CONTENT':content,'GLOSSARY':glossary_html(item.get('glossary')),'PAGE_CONTEXT':page_context_html(item, entries),'RELATED':related,'CTA_TITLE':e(item.get('cta_title','Quer aplicar tecnologia ao seu contexto?')),'CTA_TEXT':e(item.get('cta_text','Conheça a forma como a Koddahub entende o problema antes de propor uma solução.')),'CTA_URL':e(cta_url),'CTA_LABEL':e(item.get('cta_label','Como trabalhamos')),'CTA_CLASS':'btn-success' if is_whatsapp else 'btn-brand','CTA_ATTRS':' target="_blank" rel="noopener"' if is_whatsapp else '','CTA_ICON':cta_icon}.items():
            body = body.replace('{{'+key+'}}', value)
        schema = {"@context":"https://schema.org","@type":"BlogPosting","headline":item['title'],"description":item['meta_description'],"datePublished":str(item['publish_date']),"author":{"@type":"Organization","name":"Koddahub"},"mainEntityOfPage":url}
        if item.get('modified_date'):
            schema['dateModified'] = str(item['modified_date'])
        schema['image'] = site_url + cover_path
        page = shell(home, body, item['seo_title'], item['meta_description'], url, site_url, version, schema, True, cover_path)
        target_dir = target/item['slug']; target_dir.mkdir(exist_ok=True)
        (target_dir/'index.html').write_text(page, encoding='utf-8')
    return [blog_url] + [blog_url + item['slug'] + '/' for item in entries]
