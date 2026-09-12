import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from blog import articles, build_blog, markdown

ROOT = Path(__file__).resolve().parents[1]

class BlogTests(unittest.TestCase):
    def test_draft_stays_private(self):
        self.assertNotIn("boas-vindas-blog-koddahub", {entry["slug"] for entry in articles()})

    def test_numbered_list_keeps_items_and_wrapped_lines(self):
        rendered = markdown("1. **Primeira pergunta?** Texto\n2. **Segunda pergunta?** Linha\n   continua aqui.")
        self.assertIn('<ol>', rendered)
        self.assertIn('<li><strong>Primeira pergunta?</strong> Texto</li>', rendered)
        self.assertIn('<li><strong>Segunda pergunta?</strong> Linha continua aqui.</li>', rendered)
        self.assertEqual(rendered.count('<li>'), 2)

    def test_published_article_and_seo(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            (source/'example.md').write_text('''---
title: Exemplo editorial
seo_title: Exemplo editorial | Blog Koddahub
meta_description: Artigo de teste do blog.
summary: Resumo verificável.
category: Automação
reading_time: 2 minutos
slug: exemplo-editorial
status: published
publish_date: 2026-01-01
---
# Exemplo editorial

Texto de teste.
''', encoding='utf-8')
            self.assertEqual(len(articles(source, date(2026, 1, 2))), 1)
            self.assertEqual(len(articles(source, date(2025, 12, 31))), 0)
            home = (ROOT/'public/index.template.html').read_text(encoding='utf-8').replace('{{YEAR}}','2026').replace('{{ASSET_VERSION}}','test').replace('{{SITE_URL}}','https://koddahub.com.br').replace('{{CHAT_WEBHOOK_URL}}','')
            urls = build_blog(source, home, 'https://koddahub.com.br', 'test', source)
            listing = (source/'blog/index.html').read_text()
            page = (source/'blog/exemplo-editorial/index.html').read_text()
            self.assertIn('/blog/exemplo-editorial/', urls[1])
            self.assertIn('Exemplo editorial', listing)
            self.assertIn('<title>Exemplo editorial | Blog Koddahub</title>', page)
            self.assertIn('rel="canonical" href="https://koddahub.com.br/blog/exemplo-editorial/"', page)
            self.assertIn('name="description" content="Artigo de teste do blog."', page)
            self.assertIn('BlogPosting', page)
            self.assertIn('<h1>Exemplo editorial</h1>', page)

if __name__ == '__main__':
    unittest.main()
