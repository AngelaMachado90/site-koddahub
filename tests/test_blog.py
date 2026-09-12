import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from blog import articles, build_blog, card_html, markdown, source_links
from publish_due import due_articles

ROOT = Path(__file__).resolve().parents[1]

class BlogTests(unittest.TestCase):
    def test_draft_stays_private(self):
        self.assertNotIn("boas-vindas-blog-koddahub", {entry["slug"] for entry in articles()})

    def test_scheduled_article_waits_for_its_date(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            (source / "scheduled.md").write_text('''---
title: Pauta programada
seo_title: Pauta programada
meta_description: Texto programado.
summary: Resumo.
category: Automação
reading_time: 2 minutos
slug: pauta-programada
status: scheduled
publish_date: 2026-09-13
---
# Pauta programada

Conteúdo.
''', encoding="utf-8")
            self.assertEqual(articles(source, date(2026, 9, 12)), [])
            self.assertEqual([entry["slug"] for entry in articles(source, date(2026, 9, 13))], ["pauta-programada"])

    def test_numbered_list_keeps_items_and_wrapped_lines(self):
        rendered = markdown("1. **Primeira pergunta?** Texto\n2. **Segunda pergunta?** Linha\n   continua aqui.")
        self.assertIn('<ol>', rendered)
        self.assertIn('<li><strong>Primeira pergunta?</strong> Texto</li>', rendered)
        self.assertIn('<li><strong>Segunda pergunta?</strong> Linha continua aqui.</li>', rendered)
        self.assertEqual(rendered.count('<li>'), 2)

    def test_due_articles_waits_and_detects_missed_date(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scheduled = root / "scheduled"
            scheduled.mkdir()
            (scheduled / "one.md").write_text("---\nstatus: scheduled\npublish_date: 2026-09-13\nslug: one\n---\n")
            self.assertEqual(due_articles(date(2026, 9, 12), scheduled, root), [])
            self.assertEqual(len(due_articles(date(2026, 9, 13), scheduled, root)), 1)
            with self.assertRaises(RuntimeError):
                due_articles(date(2026, 9, 14), scheduled, root)
            target = root / "blog/one/index.html"
            target.parent.mkdir(parents=True)
            target.write_text("ok")
            self.assertEqual(due_articles(date(2026, 9, 14), scheduled, root), [])

    def test_sources_are_linked_without_editorial_notes(self):
        rendered = source_links("## Referências para revisão\n\nDocumentação: https://docs.n8n.io/ e texto interno.")
        self.assertIn('href="https://docs.n8n.io/"', rendered)
        self.assertNotIn('texto interno', rendered)

    def test_card_uses_article_cover_when_available(self):
        item = {"title": "Artigo com imagem", "slug": "artigo-com-imagem", "publish_date": date(2026, 9, 12), "category": "Atendimento", "summary": "Resumo com imagem.", "reading_time": "15 minutos", "cover": "/assets/images/blog/exemplo.jpg", "cover_width": 1880, "cover_height": 1255}
        rendered = card_html(item, position=2)
        self.assertIn('blog-card-media--cover', rendered)
        self.assertIn('src="/assets/images/blog/exemplo.jpg"', rendered)
        self.assertIn('alt=""', rendered)

    def test_responsive_article_is_featured_with_its_cover(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            home = (ROOT/'public/index.template.html').read_text(encoding='utf-8').replace('{{YEAR}}','2026').replace('{{ASSET_VERSION}}','test').replace('{{SITE_URL}}','https://koddahub.com.br').replace('{{CHAT_WEBHOOK_URL}}','')
            build_blog(target, home, 'https://koddahub.com.br', 'test', ROOT/'docs/editorial/publicados')
            listing = (target/'blog/index.html').read_text(encoding='utf-8')
            featured = listing.split('class="card blog-card blog-featured"', 1)[1].split('</article>', 1)[0]
            self.assertIn('href="/blog/site-responsivo-como-oferecer-uma-boa-experiencia-em-cada-tela/"', featured)
            self.assertIn('src="/assets/images/blog/site-responsivo.jpg"', featured)

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
