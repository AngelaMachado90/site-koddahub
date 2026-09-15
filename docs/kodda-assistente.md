# Kodda — assistente didático do Blog Koddahub

VAL produz o artigo e seu glossário estruturado no front matter editorial.
O build usa essa fonte única para gerar o “Glossário rápido” visível e o
contexto JSON consumido pela Kodda. Não replique definições manualmente no
JavaScript.

## Prioridade e intenção

A resposta local consulta primeiro o glossário do artigo aberto e depois o
glossário agregado dos artigos publicados. Em seguida, pode indicar conteúdo
relacionado; quando não encontra resposta confiável, usa fallback controlado.
As intenções cobertas no piloto são conceito de glossário, pergunta comparativa,
conteúdo relacionado, interesse comercial e termo desconhecido.

O frontend envia ao webhook `message`, `sessionId` e `context`, com tipo e URL
da página e, quando disponível, slug, título e categoria. O backend/n8n deve
usar o slug para buscar artigo e glossário na fonte publicada. A URL do webhook
continua sem credenciais e o contrato não autoriza registrar conversa ou dados
pessoais desnecessários.

## Resposta e interface

Uma resposta conceitual mostra definição curta. “Ver exemplo” ou “Explique
mais” revela exemplo e aplicação. Até três termos relacionados aparecem como
quick replies. Comparações usam pares empilháveis. O botão verde do WhatsApp
permanece separado e ganha contexto somente depois de uma resposta relevante;
o envio continua dependendo da confirmação da pessoa no WhatsApp.

O artigo piloto é `dado-metrica-e-kpi-diferencas-que-ajudam-a-decidir-melhor`.
Seu glossário contém dado, dados quantitativo e qualitativo, métrica, KPI,
indicador, valor zero e dado ausente. Cada card oferece “Perguntar ao Kodda”.

## Estados e validação

- início: saudação contextual e até três sugestões do artigo;
- loading: indicador “Kodda está explicando” e envio bloqueado;
- sucesso: card curto, expansão opcional e quick replies;
- erro: mensagem sem detalhe técnico, opção para recuperar a pergunta e CTA
  persistente separado;
- desconhecido: informa que o termo não foi encontrado, sem inventar definição.

Validar o fallback com `node --test tests/test_chat_fallback.js`, o blog com
`python3 -m unittest discover -s tests -v` e o artefato com
`python3 scripts/build.py`. Em browser, conferir abertura, expansão, chips,
accordion, foco, scroll e o botão do WhatsApp em 390, 360 e 320 pixels.

## Contrato do glossário editorial

Cada item de `glossary` exige `term`, `definition`, `example` e `application`.
`aliases` melhora o reconhecimento de variações, e `related` alimenta no máximo
três chips quando os termos também existem no catálogo publicado. O build
interrompe se um campo obrigatório estiver ausente.
