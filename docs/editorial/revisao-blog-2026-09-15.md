# Revisão editorial do Blog Koddahub — 15/09/2026

## Escopo e critério

Inventário dos dez artigos publicados ou elegíveis em 15/09/2026. A revisão
preservou slugs e datas reais, separou título editorial de SEO title e avaliou
clareza, exemplos, glossário, visual didático, CTA, cards e leitura mobile.
`AJUSTADO` identifica alteração desta rodada; `REVISADO` confirma consistência
de um artigo já trabalhado anteriormente.

## Inventário editorial

| Artigo | Título anterior | Título novo | Categoria | Tags | UX | Glossário | Visuais |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Integração entre sistemas | Integração entre sistemas: como evitar retrabalho e informação duplicada | Quando seus sistemas não conversam | Integração | Integração, APIs, Dados, Processos | AJUSTADO | 4 termos | Pipeline entre sistemas |
| RPA | Descomplicando a TI: o que é RPA e quando usar? | O que é RPA? | Automação | RPA, Automação, Processos | AJUSTADO | 4 termos | Comparação manual/RPA |
| Antes de automatizar | Antes de automatizar: cinco perguntas para entender o processo | Antes de automatizar, entenda o processo | Automação | Automação, Processos | AJUSTADO | 4 termos | Fluxo de quatro etapas |
| Streamlit | Streamlit: quando usar para transformar dados em uma aplicação útil | Quando usar Streamlit? | Dados | Streamlit, Dados, Desenvolvimento | AJUSTADO | 4 termos | Pipeline de dados à aplicação |
| Site responsivo | Site responsivo: como oferecer uma boa experiência em cada tela | Seu site funciona em qualquer tela? | Desenvolvimento | Sites, Responsividade, UX/UI | AJUSTADO | 4 termos | Cards por tipo de tela |
| Chatbot | Chatbot no atendimento: o que automatizar sem perder o contexto da conversa | Até onde um chatbot deve automatizar? | Automação | Chatbots, Atendimento, Automação, UX/UI | AJUSTADO | 4 termos | Comparação bot/pessoa |
| GA4 e n8n | n8n e GA4: como coletar dados de tráfego e eventos com critérios claros | Conectando GA4 ao n8n | Dados | n8n, GA4, Analytics, Automação | AJUSTADO | 4 termos | Pipeline GA4 ao dashboard |
| Google Ads e n8n | n8n e Google Ads: como coletar dados de campanhas para uma visão única do tráfego | Conectando Google Ads ao n8n | Dados | n8n, Google Ads, Automação, Analytics | AJUSTADO | 4 termos | Pipeline da campanha à análise |
| n8n | n8n na prática: quando faz sentido automatizar um processo com a ferramenta | Quando vale a pena usar n8n? | Automação | n8n, Automação, Processos, Integração | AJUSTADO | 4 termos | Estrutura mínima do workflow |
| Dado, métrica e KPI | Dado, métrica e KPI: diferenças que ajudam a decidir melhor | Dado, métrica ou KPI? | Dados | Dados, Analytics, Processos | REVISADO | 10 termos | 12 recursos didáticos |

## Decisões aplicadas

- O H1 e os cards usam títulos humanos de quatro a sete palavras; `seo_title`,
  meta description e conteúdo preservam a intenção de busca.
- Os slugs publicados permaneceram intactos. Nenhum redirect foi necessário.
- Cada artigo recebeu categoria controlada, de duas a quatro tags e CTA ligado
  ao tema.
- Os nove artigos sem apoio didático receberam um glossário estruturado e um
  visual com título, legenda, alt text e classificação de dados.
- O glossário do front matter continua como única fonte consumida pelo build e
  pela Kodda.

## Próximo passo

Implementar filtros do Blog por categoria e tags usando `data-category` e
`data-tags` já publicados nos cards.
