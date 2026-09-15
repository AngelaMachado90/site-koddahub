#!/usr/bin/env python3
"""Gera a versao publica do site KoddaHub em dist/."""

import json
import os
import shutil
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from blog import build_blog, google_tag, social_links_html

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
TEMPLATE = PUBLIC / "index.template.html"
SITE_CONFIG = ROOT / "config/site.json"


def environment_url(name: str, default: str = "", *, required: bool = False) -> str:
    value = os.environ.get(name, default).strip()
    if required and not value:
        raise ValueError(f"{name} precisa ser informado")
    if value:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"{name} precisa ser uma URL HTTP(S) valida")
    return value


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(PUBLIC, DIST, ignore=shutil.ignore_patterns("*.template.html"))
    version = os.environ.get("ASSET_VERSION", datetime.now().strftime("%Y%m%d%H%M%S"))
    site_url = environment_url("SITE_URL", "https://koddahub.com.br", required=True).rstrip("/")
    chat_webhook_url = environment_url("CHAT_WEBHOOK_URL")
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{GA4_TAG}}", google_tag())
    html = html.replace("{{YEAR}}", str(datetime.now().year))
    html = html.replace("{{ASSET_VERSION}}", version)
    html = html.replace("{{SITE_URL}}", site_url)
    html = html.replace("{{CHAT_WEBHOOK_URL}}", escape(chat_webhook_url, quote=True))
    config = json.loads(SITE_CONFIG.read_text(encoding="utf-8"))
    html = html.replace("{{SOCIAL_LINKS}}", social_links_html(config.get("social_links")))
    (DIST / "index.html").write_text(html, encoding="utf-8")
    urls = build_blog(DIST, html, site_url, version)
    (DIST / "version.txt").write_text(version, encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{url}</loc></url>\n' for url in [site_url + '/', *urls]) + '</urlset>\n',
        encoding="utf-8",
    )
    # O agendador publica como dono do projeto; builds administrativos não podem
    # deixar dist/ sem permissão de escrita para a próxima execução.
    if os.geteuid() == 0:
        owner = ROOT.stat()
        for path in (DIST, *DIST.rglob("*")):
            os.chown(path, owner.st_uid, owner.st_gid)
    print(f"Build concluido: {DIST}")

if __name__ == "__main__":
    build()
