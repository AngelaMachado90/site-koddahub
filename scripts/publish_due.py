#!/usr/bin/env python3
"""Publica somente artigos agendados que vencem hoje no servidor Koddahub."""

import fcntl
import os
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEDULED = ROOT / "docs/editorial/agendados"
DIST = ROOT / "dist"
PRODUCTION = Path("/home/kodda/public_html")
BACKUPS = Path("/home/kodda/site-koddahub-backups")
LOCK = Path("/home/kodda/.local/state/site-koddahub-publish.lock")


def due_articles(today: date, scheduled: Path = SCHEDULED, production: Path = PRODUCTION):
    due = []
    for path in scheduled.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            raise ValueError(f"Front matter ausente: {path}")
        metadata = yaml.safe_load(content.split("---\n", 2)[1])
        if metadata.get("status") != "scheduled":
            continue
        planned = date.fromisoformat(str(metadata["publish_date"]))
        target = production / "blog" / str(metadata["slug"]) / "index.html"
        if planned < today and not target.is_file():
            raise RuntimeError(f"Agendamento vencido sem publicação; revisar data real: {path}")
        if planned == today and not target.is_file():
            due.append((path, target))
    return due


def publish(today: date = None):
    today = today or date.today()
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        due = due_articles(today)
        if not due:
            print(f"{today}: nenhum artigo novo para publicar")
            return 0
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], cwd=ROOT, check=True)
        for _, target in due:
            built = DIST / target.relative_to(PRODUCTION)
            if not built.is_file():
                raise RuntimeError(f"Build não gerou artigo devido: {built}")
        backup = BACKUPS / datetime.now().strftime("%Y%m%d-%H%M%S")
        backup.mkdir(parents=True, exist_ok=False)
        shutil.copytree(PRODUCTION / "blog", backup / "blog")
        shutil.copy2(PRODUCTION / "sitemap.xml", backup / "sitemap.xml")
        try:
            subprocess.run(["rsync", "-a", "--delete", str(DIST / "blog") + "/", str(PRODUCTION / "blog") + "/"], check=True)
            temporary = PRODUCTION / "sitemap.xml.new"
            shutil.copy2(DIST / "sitemap.xml", temporary)
            os.replace(temporary, PRODUCTION / "sitemap.xml")
            for _, target in due:
                if not target.is_file():
                    raise RuntimeError(f"Artigo ausente depois da cópia: {target}")
        except Exception:
            subprocess.run(["rsync", "-a", "--delete", str(backup / "blog") + "/", str(PRODUCTION / "blog") + "/"], check=True)
            shutil.copy2(backup / "sitemap.xml", PRODUCTION / "sitemap.xml")
            raise
        print(f"{today}: {len(due)} artigo(s) publicado(s); backup: {backup}")
        return len(due)


if __name__ == "__main__":
    publish()
