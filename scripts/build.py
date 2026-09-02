#!/usr/bin/env python3
"""Gera a versao publica do site KoddaHub em dist/."""

import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
TEMPLATE = PUBLIC / "index.template.html"

def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(PUBLIC, DIST, ignore=shutil.ignore_patterns("*.template.html"))
    version = os.environ.get("ASSET_VERSION", datetime.now().strftime("%Y%m%d%H%M%S"))
    site_url = os.environ.get("SITE_URL", "https://koddahub.com.br").rstrip("/")
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{YEAR}}", str(datetime.now().year))
    html = html.replace("{{ASSET_VERSION}}", version)
    html = html.replace("{{SITE_URL}}", site_url)
    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "version.txt").write_text(version, encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{site_url}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n</urlset>\n',
        encoding="utf-8",
    )
    print(f"Build concluido: {DIST}")

if __name__ == "__main__":
    build()
