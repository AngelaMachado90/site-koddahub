import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from blog import articles, build_blog, card_html, markdown, related_articles, source_links
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

    def test_new_article_requires_fifteen_minutes_of_actual_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            article = source / 'short.md'
            article.write_text('''---
title: Pauta curta
seo_title: Pauta curta
meta_description: Exemplo.
summary: Exemplo.
category: Dados
reading_time: 15 minutos
slug: pauta-curta
status: scheduled
publish_date: 2026-09-15
---
# Pauta curta

Texto insuficiente.
''', encoding='utf-8')
            self.assertEqual(articles(source, date(2026, 9, 14)), [])
            with self.assertRaisesRegex(ValueError, 'mínimo de 2250 palavras'):
                articles(source, date(2026, 9, 15))
            article.write_text(article.read_text(encoding='utf-8').replace('Texto insuficiente.', ' '.join(['exemplo'] * 2250)), encoding='utf-8')
            self.assertEqual(len(articles(source, date(2026, 9, 15))), 1)

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

    def test_related_articles_use_published_editorial_links(self):
        current = {'slug': 'current', 'category': 'Automação', 'publish_date': date(2026, 9, 14),
                   'body': '## Links internos sugeridos\n\n- /blog/guide/\n- /blog/future/\n- /blog/current/'}
        guide = {'slug': 'guide', 'category': 'Dados', 'publish_date': date(2026, 9, 1), 'body': ''}
        similar = {'slug': 'similar', 'category': 'Automação', 'publish_date': date(2026, 9, 2), 'body': ''}
        selected = related_articles(current, [current, guide, similar], limit=2)
        self.assertEqual([item['slug'] for item in selected], ['guide', 'similar'])

    def test_card_uses_article_cover_when_available(self):
        item = {"title": "Artigo com imagem", "slug": "artigo-com-imagem", "publish_date": date(2026, 9, 12), "category": "Atendimento", "summary": "Resumo com imagem.", "reading_time": "15 minutos", "cover": "/assets/images/blog/exemplo.jpg", "cover_width": 1880, "cover_height": 1255}
        rendered = card_html(item, position=2)
        self.assertIn('blog-card-media--cover', rendered)
        self.assertIn('src="/assets/images/blog/exemplo.jpg"', rendered)
        self.assertIn('alt=""', rendered)

    def test_latest_article_is_featured_with_its_cover(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            home = (ROOT/'public/index.template.html').read_text(encoding='utf-8').replace('{{YEAR}}','2026').replace('{{ASSET_VERSION}}','test').replace('{{SITE_URL}}','https://koddahub.com.br').replace('{{CHAT_WEBHOOK_URL}}','')
            build_blog(target, home, 'https://koddahub.com.br', 'test', ROOT/'docs/editorial/publicados')
            listing = (target/'blog/index.html').read_text(encoding='utf-8')
            featured = listing.split('class="card blog-card blog-featured"', 1)[1].split('</article>', 1)[0]
            self.assertIn('href="/blog/integracao-entre-sistemas-como-evitar-retrabalho-e-informacao-duplicada/"', featured)
            self.assertIn('src="/assets/images/blog/integracao-entre-sistemas.webp"', featured)
            self.assertIn('<h2 id="blog-more-title">Outras publicações</h2>', listing)
            self.assertLess(listing.index('class="card blog-card blog-featured"'), listing.index('id="blog-more-title"'))
            self.assertLess(listing.index('id="blog-more-title"'), listing.index('<div class="row g-4">', listing.index('id="blog-more-title"')))
            chatbot = (target/'blog/chatbot-no-atendimento-o-que-automatizar-sem-perder-o-contexto-da-conversa/index.html').read_text(encoding='utf-8')
            self.assertIn('src="/assets/images/blog/chatbot-automacao-contexto.webp"', chatbot)
            self.assertIn('property="og:image" content="https://koddahub.com.br/assets/images/blog/chatbot-automacao-contexto.webp"', chatbot)
            n8n = (target/'blog/n8n-na-pratica-quando-faz-sentido-automatizar-um-processo-com-a-ferramenta/index.html').read_text(encoding='utf-8')
            self.assertIn('src="/assets/images/blog/n8n-workflow-automacao.webp"', n8n)
            self.assertIn('property="og:image" content="https://koddahub.com.br/assets/images/blog/n8n-workflow-automacao.webp"', n8n)
            rpa = (target/'blog/descomplicando-a-ti-o-que-e-rpa/index.html').read_text(encoding='utf-8')
            headings = ['O que é?', 'Exemplo simples', 'Por que importa?', 'Como funciona?', 'Exemplo real', 'O que fazer com isso?']
            positions = [rpa.index(f'<h2>{heading}</h2>') for heading in headings]
            self.assertEqual(positions, sorted(positions))

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
cover: /assets/images/blog/n8n-workflow-automacao.webp
cover_alt: Fluxo de automação ilustrado
cover_width: 1672
cover_height: 941
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
            self.assertIn('/assets/vendor/bootstrap/bootstrap.bundle.min.js?v=test', listing)
            self.assertIn('/assets/js/chat-fallback.js?v=test', listing)
            self.assertIn('/assets/js/site.js?v=test', listing)
            self.assertIn('src="/assets/images/logo/kodda-chat-avatar-128.webp"', listing)
            self.assertEqual(listing.count('https://www.googletagmanager.com/gtag/js?id=G-3DNTXV2CYK'), 1)
            self.assertIn("gtag('config', 'G-3DNTXV2CYK')", listing)
            self.assertIn('<title>Exemplo editorial | Blog Koddahub</title>', page)
            self.assertEqual(page.count('https://www.googletagmanager.com/gtag/js?id=G-3DNTXV2CYK'), 1)
            self.assertIn('/assets/js/site.js?v=test', page)
            self.assertIn('rel="canonical" href="https://koddahub.com.br/blog/exemplo-editorial/"', page)
            self.assertIn('name="description" content="Artigo de teste do blog."', page)
            self.assertIn('BlogPosting', page)
            self.assertIn('"mainEntityOfPage": "https://koddahub.com.br/blog/exemplo-editorial/"', page)
            self.assertIn('<h1>Exemplo editorial</h1>', page)

    def test_public_article_without_cover_blocks_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            (source/'no-cover.md').write_text('''---
title: Artigo sem capa
seo_title: Artigo sem capa
meta_description: Exemplo.
summary: Exemplo.
category: Automação
reading_time: 2 minutos
slug: artigo-sem-capa
status: published
publish_date: 2026-01-01
---
# Artigo sem capa
''', encoding='utf-8')
            home = (ROOT/'public/index.template.html').read_text(encoding='utf-8').replace('{{YEAR}}','2026').replace('{{ASSET_VERSION}}','test').replace('{{SITE_URL}}','https://koddahub.com.br').replace('{{CHAT_WEBHOOK_URL}}','')
            with self.assertRaisesRegex(ValueError, 'Artigo sem capa'):
                build_blog(source, home, 'https://koddahub.com.br', 'test', source)

if __name__ == '__main__':
    unittest.main()
