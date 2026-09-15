# Diretrizes didáticas da VAL

Este documento é o contrato de clareza aplicado ao repositório. O padrão
operacional completo da persona fica na referência canônica
`redator-blog-koddahub/references/ux-editorial.md`; campos, taxonomia, build e
publicação ficam em `docs/blog.md`. Essa separação evita cópias divergentes da
mesma regra.

O princípio editorial é: **descomplicar tecnologia sem empobrecer o conceito**.
O leitor não precisa ser desenvolvedor, analista ou especialista para entender
um artigo do Blog Koddahub.

## Progressão da explicação

Ao introduzir um conceito técnico, use esta ordem:

1. **Conceito:** definição curta em linguagem comum.
2. **Exemplo:** situação cotidiana e reconhecível.
3. **Aplicação:** para que serve e qual problema ou decisão apoia.
4. **Detalhe técnico:** funcionamento, variações, limites e cuidados.

Exemplos devem preferir situações com pedidos, clientes, vendas, WhatsApp,
formulários, atendimento, sites, estoque ou tempo de resposta quando forem
adequadas ao tema. Casos hipotéticos devem ser identificados como tal; não
inventar cliente, resultado ou métrica.

## Estrutura e parágrafos

Separe conceitos diferentes em H2 ou H3. Cada parágrafo deve desenvolver uma
ideia principal. Se começar explicando um conceito e terminar em outro, divida.
Use listas e comparações quando facilitarem a consulta e evite paredes de texto.

Defina o termo antes de aprofundá-lo. Substitua jargão por linguagem comum
quando isso preservar a precisão; quando o termo técnico for necessário,
explique-o na primeira ocorrência.

## Teste de clareza antes de publicar

- uma pessoa não técnica consegue entender o conceito principal?
- cada conceito novo possui definição curta, exemplo e aplicação?
- a explicação vem antes do aprofundamento técnico?
- existem parágrafos longos ou com ideias misturadas?
- conceitos diferentes estão separados por subtítulos?
- existe jargão que pode ser substituído ou explicado?
- os exemplos são concretos e coerentes?

Se alguma resposta indicar dificuldade, o texto volta para revisão. A contagem
de palavras e o tempo estimado de leitura não substituem este teste.

## Gate para conteúdo futuro

O fluxo obrigatório é pauta → SEO → didática → UX editorial → glossário →
visual → taxonomia → CTA → QA responsivo → build → agendamento ou publicação.
Uma falha crítica mantém o conteúdo em `review`. O relatório da pauta registra
somente decisões e evidências específicas; não replica o padrão completo.
