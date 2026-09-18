import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from blog import article_share_html, article_taxonomy_html, articles, build_blog, card_html, didactic_visual_html, glossary_context, glossary_html, markdown, normalized_term, page_context_html, related_articles, social_links_html, source_links
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
tags: [Automação, Processos]
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
tags: [Dados, Analytics]
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
            with self.assertRaisesRegex(ValueError, 'sem cover'):
                articles(source, date(2026, 9, 15))

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

    def test_incomplete_future_articles_are_held_for_review(self):
        scheduled = ROOT/'docs/editorial/agendados'
        review_items = []
        for path in scheduled.glob('*.md'):
            content = path.read_text(encoding='utf-8')
            metadata = __import__('yaml').safe_load(content.split('---\n', 2)[1])
            if metadata.get('status') == 'review':
                review_items.append(metadata)
        self.assertEqual(len(review_items), 23)
        for item in review_items:
            self.assertGreaterEqual(len(item['title'].split()), 4)
            self.assertLessEqual(len(item['title'].split()), 9)
            self.assertGreaterEqual(len(item['tags']), 2)
            self.assertTrue(item['review_blockers'])
        self.assertEqual(due_articles(date(2026, 9, 16), scheduled, ROOT/'dist'), [])

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

    def test_related_articles_rank_tag_affinity_before_category_and_date(self):
        current = {'slug': 'current', 'category': 'Automação', 'tags': ['n8n', 'Google Ads'],
                   'publish_date': date(2026, 9, 14), 'body': ''}
        same_category = {'slug': 'same-category', 'category': 'Automação', 'tags': ['Processos', 'RPA'],
                         'publish_date': date(2026, 9, 13), 'body': ''}
        two_shared_tags = {'slug': 'two-shared-tags', 'category': 'Dados', 'tags': ['n8n', 'Google Ads'],
                           'publish_date': date(2026, 8, 1), 'body': ''}
        one_shared_tag = {'slug': 'one-shared-tag', 'category': 'Integração', 'tags': ['n8n', 'APIs'],
                          'publish_date': date(2026, 9, 12), 'body': ''}
        selected = related_articles(current, [current, same_category, one_shared_tag, two_shared_tags])
        self.assertEqual([item['slug'] for item in selected], ['two-shared-tags', 'one-shared-tag', 'same-category'])

    def test_article_glossary_is_visible_and_available_to_kodda(self):
        entries = articles(ROOT/'docs/editorial', date(2026, 9, 15))
        item = next(entry for entry in entries if entry['slug'] == 'dado-metrica-e-kpi-diferencas-que-ajudam-a-decidir-melhor')
        rendered = glossary_html(item['glossary'])
        context = page_context_html(item, entries)
        self.assertIn('Glossário rápido', rendered)
        self.assertIn('data-glossary-term="KPI"', rendered)
        self.assertIn('"article_slug": "dado-metrica-e-kpi-diferencas-que-ajudam-a-decidir-melhor"', context)
        self.assertIn('"term": "Dado qualitativo"', context)
        self.assertIn('"id": "conceito-ate-decisao"', context)
        self.assertIn('"normalized_term": "kpi"', context)

    def test_glossary_context_normalizes_without_changing_editorial_term(self):
        payload = glossary_context([{'term': 'Métrica', 'aliases': ['MÉTRICAS', 'metrica']}])
        self.assertEqual(payload[0]['term'], 'Métrica')
        self.assertEqual(payload[0]['normalized_term'], 'metrica')
        self.assertEqual(payload[0]['normalized_aliases'], ['metricas', 'metrica'])
        self.assertEqual(normalized_term('  KPI... o que é?! '), 'kpi o que e')

    def test_didactic_visual_is_semantic_and_escaped(self):
        visual = didactic_visual_html({
            'type': 'flow', 'title': 'Dado até decisão',
            'caption': 'Explica a progressão.', 'alt': 'Dado segue para métrica.',
            'data_kind': 'NÃO SE APLICA',
            'items': [{'label': 'Dado', 'detail': '<registro>'}, {'label': 'Métrica', 'detail': 'Medida'}],
        })
        rendered = markdown('Antes.\n\n[[visual:fluxo]]\n\nDepois.', {'fluxo': visual})
        self.assertIn('<figure class="blog-visual blog-visual--flow">', rendered)
        self.assertIn('role="img" aria-label="Dado segue para métrica."', rendered)
        self.assertIn('&lt;registro&gt;', rendered)
        self.assertNotIn('<registro>', rendered)

    def test_editorial_image_has_accessible_metadata_and_source_credit(self):
        visual = didactic_visual_html({
            'type': 'image', 'title': 'ChatGPT em uso',
            'caption': 'Exemplo de uso.', 'alt': 'Dois monitores exibindo o ChatGPT.',
            'data_kind': 'NÃO SE APLICA',
            'src': '/assets/images/blog/chatgpt.webp', 'width': 1600, 'height': 1067,
            'credit': 'Melih Can', 'source_url': 'https://www.pexels.com/pt-br/foto/16416871/',
        })
        self.assertIn('class="blog-editorial-image"', visual)
        self.assertIn('alt="Dois monitores exibindo o ChatGPT."', visual)
        self.assertIn('width="1600" height="1067"', visual)
        self.assertIn('loading="lazy" decoding="async"', visual)
        self.assertIn('Melih Can/Pexels', visual)
        self.assertIn('rel="noopener noreferrer"', visual)

    def test_step_badges_keep_accessible_brand_contrast_and_size(self):
        css = (ROOT/'public/assets/css/blog.css').read_text(encoding='utf-8')
        self.assertIn('.blog-flow-node .blog-step-number{', css)
        rule = css.split('.blog-flow-node .blog-step-number{', 1)[1].split('}', 1)[0]
        self.assertIn('width:3rem', rule)
        self.assertIn('height:3rem', rule)
        self.assertIn('background:var(--kdh-primary)', rule)
        self.assertIn('color:var(--kdh-text-inverse)', rule)
        self.assertIn('font-weight:800', rule)
        self.assertIn('line-height:1', rule)

    def test_comparison_table_has_responsive_semantic_contract(self):
        visual = didactic_visual_html({
            'type': 'table', 'title': 'Comparação', 'caption': 'Legenda.',
            'alt': 'Comparação acessível.', 'data_kind': 'EXEMPLO ILUSTRATIVO',
            'headers': ['Conceito', 'O que é', 'Exemplo'],
            'rows': [['Métrica', 'Medida calculada', '90 pedidos']],
        })
        self.assertIn('<div class="blog-comparison">', visual)
        self.assertIn('<table class="table blog-comparison__table">', visual)
        self.assertIn('<th scope="col">Conceito</th>', visual)
        self.assertIn('<th scope="row">Métrica</th>', visual)
        self.assertIn('<td data-label="O que é">Medida calculada</td>', visual)

    def test_dense_article_renders_all_visual_learning_components(self):
        entries = articles(ROOT/'docs/editorial', date(2026, 9, 15))
        item = next(entry for entry in entries if entry['slug'] == 'dado-metrica-e-kpi-diferencas-que-ajudam-a-decidir-melhor')
        components = {visual['id']: didactic_visual_html(visual) for visual in item['didactic_visuals']}
        rendered = markdown(item['body'], components)
        self.assertEqual(rendered.count('<figure class="blog-visual '), 12)
        for visual_type in ('numbered_grid', 'timeline_compare', 'dot_plot', 'pipeline', 'dashboard', 'checklist', 'steps'):
            self.assertIn(f'blog-visual--{visual_type}', rendered)
        self.assertIn('EXEMPLO ILUSTRATIVO — DADOS FICTÍCIOS', rendered)
        self.assertIn('role="img" aria-label="Gráfico de tempos de resposta', rendered)

    def test_card_uses_article_cover_when_available(self):
        item = {"title": "Artigo com imagem", "slug": "artigo-com-imagem", "publish_date": date(2026, 9, 12), "category": "Automação", "tags": ["Chatbots", "Atendimento"], "summary": "Resumo com imagem.", "reading_time": "15 minutos", "cover": "/assets/images/blog/exemplo.jpg", "cover_width": 1880, "cover_height": 1255}
        rendered = card_html(item, position=2)
        self.assertIn('blog-card-media--cover', rendered)
        self.assertIn('src="/assets/images/blog/exemplo.jpg"', rendered)
        self.assertIn('alt=""', rendered)
        self.assertIn('data-category="automacao"', rendered)
        self.assertIn('data-tags="chatbots,atendimento"', rendered)
        self.assertIn('<span class="blog-tag">Chatbots</span>', rendered)

    def test_scoped_articles_follow_controlled_taxonomy(self):
        entries = articles(ROOT/'docs/editorial', date(2026, 9, 15))
        self.assertEqual(len(entries), 11)
        for item in entries:
            self.assertGreaterEqual(len(item['tags']), 2)
            self.assertLessEqual(len(item['tags']), 5)
            self.assertLessEqual(len(item['title'].split()), 9)
            self.assertTrue(item.get('glossary'))
            self.assertTrue(item.get('didactic_visuals'))
        taxonomy = article_taxonomy_html(entries[0])
        self.assertIn('class="blog-category"', taxonomy)
        visible_tags = [tag for tag in entries[0]['tags'] if tag != entries[0]['category']]
        self.assertEqual(taxonomy.count('class="blog-tag"'), len(visible_tags))

    def test_latest_article_is_featured_with_its_cover(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            home = (ROOT/'public/index.template.html').read_text(encoding='utf-8').replace('{{YEAR}}','2026').replace('{{ASSET_VERSION}}','test').replace('{{SITE_URL}}','https://koddahub.com.br').replace('{{CHAT_WEBHOOK_URL}}','')
            build_blog(target, home, 'https://koddahub.com.br', 'test', ROOT/'docs/editorial/publicados')
            listing = (target/'blog/index.html').read_text(encoding='utf-8')
            featured = listing.split('class="card blog-card blog-featured"', 1)[1].split('</article>', 1)[0]
            latest = articles(ROOT/'docs/editorial/publicados')[0]
            self.assertIn(f'href="/blog/{latest["slug"]}/"', featured)
            self.assertIn(f'src="{latest["cover"]}', featured)
            self.assertIn('<h2 id="blog-more-title">Outras publicações</h2>', listing)
            self.assertLess(listing.index('class="card blog-card blog-featured"'), listing.index('id="blog-more-title"'))
            self.assertLess(listing.index('id="blog-more-title"'), listing.index('<div class="row g-4">', listing.index('id="blog-more-title"')))
            article = (target/'blog/e-seguro-usar-claude/index.html').read_text(encoding='utf-8')
            self.assertIn('src="/assets/images/avatars/val-avatar.webp"', article)
            self.assertLess(article.index('class="blog-cover'), article.index('class="article-share"'))
            self.assertLess(article.index('class="article-share"'), article.index('class="blog-prose"'))
            chatbot = (target/'blog/chatbot-no-atendimento-o-que-automatizar-sem-perder-o-contexto-da-conversa/index.html').read_text(encoding='utf-8')
            self.assertIn('src="/assets/images/blog/chatbot-automacao-contexto.webp', chatbot)
            self.assertIn('property="og:image" content="https://koddahub.com.br/assets/images/blog/chatbot-automacao-contexto.webp', chatbot)
            n8n = (target/'blog/n8n-na-pratica-quando-faz-sentido-automatizar-um-processo-com-a-ferramenta/index.html').read_text(encoding='utf-8')
            self.assertIn('src="/assets/images/blog/n8n-workflow-automacao.webp', n8n)
            self.assertIn('property="og:image" content="https://koddahub.com.br/assets/images/blog/n8n-workflow-automacao.webp', n8n)
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
tags: [Automação, Processos]
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
            self.assertIn('class="footer-brand kdh-brand-wordmark"', listing)
            self.assertIn('class="kdh-brand-kodda"', listing)
            self.assertIn('class="kdh-brand-hub"', listing)
            self.assertIn('class="footer-link"', listing)
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
tags: [Automação, Processos]
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

    def test_footer_typography_uses_design_system_tokens(self):
        css = (ROOT/'public/assets/css/style.css').read_text(encoding='utf-8')
        footer = css.split('.site-footer{', 1)[1].split('}', 1)[0]
        self.assertIn('font-family:var(--kdh-font-sans)', footer)
        self.assertIn('.site-footer p{margin:0;font-weight:var(--kdh-font-weight-regular)}', css)
        self.assertIn('font-weight:var(--kdh-font-weight-extra-bold)', css)
        self.assertIn('.footer-link{font-weight:var(--kdh-font-weight-bold)}', css)

    def test_social_links_render_only_confirmed_supported_urls(self):
        self.assertEqual(social_links_html([]), '')
        rendered = social_links_html([{'network': 'linkedin', 'url': 'https://www.linkedin.com/company/koddahub'}])
        self.assertIn('aria-label="Koddahub no LinkedIn"', rendered)
        self.assertIn('target="_blank" rel="noopener noreferrer"', rendered)
        with self.assertRaisesRegex(ValueError, 'URL oficial inválida'):
            social_links_html([{'network': 'linkedin', 'url': 'https://example.com/koddahub'}])

    def test_article_share_has_accessible_fallback_actions(self):
        rendered = article_share_html({'title': 'Artigo de exemplo'})
        self.assertIn('data-native-share hidden', rendered)
        self.assertIn('Compartilhar artigo no WhatsApp', rendered)
        self.assertIn('linkedin.com/sharing/share-offsite', rendered)
        self.assertIn('data-copy-link', rendered)
        self.assertIn('role="status" aria-live="polite"', rendered)

if __name__ == '__main__':
    unittest.main()
