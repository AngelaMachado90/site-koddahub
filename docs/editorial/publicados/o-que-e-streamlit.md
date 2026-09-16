---
title: "O que é Streamlit?"
seo_title: "O que é Streamlit e como funciona? | Koddahub"
meta_description: "Entenda o que é Streamlit, como ele transforma código Python em uma aplicação interativa e veja um exemplo simples com dados de vendas."
slug: o-que-e-streamlit
category: "Dados"
reading_time: 15 minutos
summary: "Uma introdução ao Streamlit para entender como dados, código Python e componentes de tela formam uma aplicação interativa."
planned_date: 31/08/2026
publish_date: 2026-08-31
status: published
author: VAL — Valor, Autoridade e Linguagem Koddahub
cover: /assets/images/blog/o-que-e-streamlit.webp
cover_alt: Ilustração de dados vindos de planilhas e banco para uma aplicação interativa exibida em notebook, monitor e celulares
cover_width: 1672
cover_height: 941
image_source:
  provider: OpenAI
  type: imagem gerada para o Blog Koddahub
primary_keyword: "o que é Streamlit"
related_terms:
  - "Streamlit Python"
  - "aplicação de dados"
  - "dashboard em Python"
  - "aplicação interativa"
  - "biblioteca Python"
search_intent: "Informacional"
primary_audience: "Pessoas não técnicas, gestores, analistas e profissionais que desejam entender como análises em Python podem virar aplicações interativas"
editorial_objective: "Apresentar Streamlit em linguagem simples e preparar o leitor para avaliar seus primeiros casos de uso"
funnel_stage: "Descoberta e educação"
cta_title: "Tem uma análise que poderia virar aplicação?"
cta_text: "A Koddahub pode ajudar a organizar a pergunta, os dados e o primeiro fluxo antes de transformar a ideia em uma aplicação."
cta_label: "Converse sobre sua ideia"
tags: [Streamlit, Dados, Desenvolvimento]
glossary:
- term: Streamlit
  aliases:
  - aplicação Streamlit
  definition: Biblioteca Python usada para criar aplicações interativas, principalmente para dados.
  example: Uma tabela de vendas vira uma página com filtros, indicadores e gráficos.
  application: Permite compartilhar uma análise por meio de uma interface mais fácil de usar.
  related:
  - Python
  - Widget
  - Aplicação de dados
- term: Python
  aliases:
  - linguagem Python
  definition: Linguagem de programação muito usada em dados, automação e desenvolvimento de software.
  example: Um código em Python soma vendas e calcula a média por mês.
  application: Organiza as regras que consultam, transformam e apresentam os dados.
  related:
  - Streamlit
- term: Widget
  aliases:
  - componente interativo
  definition: Controle de tela usado para receber uma escolha ou ação da pessoa.
  example: Um seletor permite escolher o mês que será analisado.
  application: Torna a aplicação interativa sem exigir que a pessoa altere o código.
  related:
  - Streamlit
  - Filtro
- term: Aplicação de dados
  aliases:
  - data app
  definition: Interface que usa dados para responder perguntas ou apoiar tarefas.
  example: Uma página mostra vendas, pedidos pendentes e produtos sem estoque.
  application: Aproxima uma análise das pessoas que precisam consultá-la ou agir sobre ela.
  related:
  - Streamlit
  - Dashboard
didactic_visuals:
- id: fluxo-introdutorio-streamlit
  type: pipeline
  title: Como uma aplicação Streamlit funciona
  caption: A aplicação recebe dados, aplica regras em Python e apresenta o resultado em componentes interativos.
  alt: Fluxo com fonte de dados, código Python, interface Streamlit e pessoa usuária.
  data_kind: NÃO SE APLICA
  items:
  - label: Dados
    detail: Planilha, banco ou API
  - label: Python
    detail: Organiza e calcula
  - label: Streamlit
    detail: Monta a interface
  - label: Pessoa
    detail: Consulta e interage
- id: tela-exemplo-vendas-streamlit
  type: dashboard
  title: Uma tela simples para acompanhar vendas
  caption: O filtro muda o período; os indicadores resumem o resultado; a tabela permite conferir os pedidos.
  alt: Esquema de aplicação com filtro de período, indicadores de vendas e pedidos e tabela de detalhes.
  data_kind: DADOS ILUSTRATIVOS
  kpi_label: Vendas no período
  kpi_value: R$ 18.500
  kpi_change: Exemplo ilustrativo
  updated: Após a escolha do período
  details:
  - label: Período
    value: Agosto
  - label: Pedidos
    value: "74"
  - label: Origem
    value: Dados ilustrativos
---
# O que é Streamlit?

Imagine que uma analista acompanha as vendas em uma planilha. Toda segunda-feira, ela atualiza os dados, aplica filtros, calcula os totais e envia uma imagem para a equipe. Quando alguém pergunta quanto foi vendido em outra região ou em outro período, a analista precisa refazer parte do trabalho.

Streamlit pode transformar essa análise em uma página interativa. Em vez de pedir uma nova imagem, a pessoa escolhe o período, consulta os indicadores e vê a tabela atualizada. A regra continua sendo escrita em Python, mas o resultado aparece em uma interface que pode ser usada sem abrir o código.

**Streamlit é uma biblioteca Python para criar aplicações interativas.** Ela é muito usada para apresentar dados, modelos e análises em uma interface com textos, filtros, tabelas, gráficos e botões.

Neste artigo, vamos entender o conceito antes dos detalhes técnicos. O exemplo de vendas é hipotético e usa números ilustrativos. Ele serve para explicar o funcionamento da ferramenta, não representa resultado de cliente.

## O que é Streamlit?

Streamlit é uma biblioteca, ou seja, um conjunto de recursos que pode ser usado em um programa Python. Ela fornece componentes prontos para montar uma interface: título, texto, campo de seleção, botão, tabela, gráfico e mensagem de status são alguns exemplos.

Pense em uma cozinha. Python representa a forma de preparar os ingredientes: buscar os dados, corrigir formatos, fazer contas e aplicar regras. Streamlit ajuda a organizar o balcão onde o resultado será apresentado e onde a pessoa poderá fazer escolhas.

Isso permite que um código usado apenas por quem programa se transforme em uma aplicação acessível pelo navegador. A pessoa não precisa alterar uma variável no arquivo para analisar outro mês. Ela usa um filtro na própria tela.

### O que significa “aplicação de dados”?

Uma aplicação de dados é uma interface criada para responder perguntas ou apoiar uma tarefa com informações registradas.

Um painel de pedidos é um exemplo. Ele pode mostrar quantos pedidos chegaram, quais estão atrasados e quais produtos precisam de reposição. A pessoa seleciona uma loja, consulta o resultado e decide o que investigar.

A aplicação não melhora os dados sozinha. Se os pedidos estão duplicados ou a regra de atraso está errada, a tela também exibirá um resultado incorreto. Streamlit facilita a interação com a análise; a qualidade ainda depende da fonte, das regras e da validação.

### Streamlit é uma linguagem de programação?

Não. A linguagem é Python. Streamlit é uma biblioteca usada dentro de um código Python.

Essa diferença ajuda a entender as responsabilidades. Python pode ler um arquivo, consultar um banco, calcular o valor vendido e ordenar os produtos. Streamlit mostra esses resultados na tela e recebe as escolhas da pessoa.

Quem desenvolve ainda precisa conhecer Python para construir e manter a aplicação. Quem usa a aplicação, porém, pode interagir com ela pelo navegador sem conhecer a linguagem.

## Um exemplo simples

Considere uma pequena empresa que quer acompanhar as vendas mensais. Ela possui uma tabela com data, número do pedido, região, produto, quantidade e valor.

Sem uma aplicação, a equipe abre o arquivo, aplica filtros e calcula os totais. Com Streamlit, pode existir uma tela com:

- um filtro de mês;
- um filtro de região;
- o valor total vendido;
- a quantidade de pedidos;
- um gráfico com a evolução diária;
- uma tabela para conferir os registros.

Quando a pessoa escolhe agosto e a região Sul, a aplicação usa essas escolhas, filtra os dados e apresenta o resultado correspondente. A interface reduz o trabalho manual de repetir a mesma análise.

O código abaixo ilustra a ideia. Os dados são fixos para manter o exemplo pequeno:

```python
import streamlit as st

st.title("Acompanhamento de vendas")

mes = st.selectbox("Escolha o mês", ["Julho", "Agosto"])

if mes == "Agosto":
    total_vendas = 18500
    total_pedidos = 74
else:
    total_vendas = 16200
    total_pedidos = 68

st.metric("Vendas no período", f"R$ {total_vendas:,.2f}")
st.metric("Pedidos", total_pedidos)
```

`st.title` cria o título. `st.selectbox` cria o seletor. `st.metric` apresenta um indicador. Em uma aplicação real, os valores viriam de uma fonte confiável e a formatação monetária seria ajustada ao público brasileiro.

O exemplo mostra a principal proposta do Streamlit: escrever comandos Python em uma ordem compreensível e apresentar o resultado como uma interface.

[[visual:tela-exemplo-vendas-streamlit]]

## Por que Streamlit importa?

Muitas análises começam em um notebook, script ou planilha e ficam concentradas em quem sabe executá-las. O resultado pode ser útil, mas pedir uma nova combinação de filtros depende dessa pessoa.

Streamlit ajuda a criar uma camada de interação. A equipe pode consultar recortes previstos, observar explicações e conferir detalhes sem editar o código.

Isso é útil para validar uma ideia. Antes de investir em um sistema maior, uma equipe pode criar uma versão pequena, observar como as pessoas usam a tela e descobrir quais perguntas realmente importam.

Também pode ser útil em ferramentas internas. Uma pessoa do atendimento pode pesquisar um pedido; uma equipe comercial pode comparar períodos; uma operação pode acompanhar itens sem estoque; uma área de dados pode compartilhar um modelo exploratório com controles claros.

O valor não está em colocar vários gráficos na página. A aplicação precisa reduzir uma dúvida, apoiar uma decisão ou facilitar uma tarefa. Se ninguém sabe o que fazer depois de olhar a tela, a interface ainda não resolveu o problema.

## Como Streamlit funciona?

Uma aplicação Streamlit normalmente começa em um arquivo Python. O arquivo importa a biblioteca, obtém os dados, aplica regras e declara os elementos que aparecerão na tela.

Quando a aplicação está em execução, o navegador mostra esses elementos para a pessoa. Ao mudar um filtro ou acionar um botão, o Streamlit pode executar o código novamente para produzir o novo resultado.

Essa reexecução torna o desenvolvimento direto: o código segue de cima para baixo e a tela acompanha esse fluxo. Ela também exige cuidado. Se o programa consultar uma fonte lenta em toda interação, a pessoa poderá esperar novamente a cada mudança.

### 1. A fonte fornece os dados

Dado é uma informação registrada. No exemplo de vendas, cada linha pode representar um pedido.

A fonte pode ser uma planilha, um arquivo, um banco de dados ou uma API. API é uma forma organizada de um sistema fornecer informações ou receber solicitações de outro sistema.

Antes de montar a interface, é necessário saber de onde vêm os dados, quando são atualizados e quem responde por sua qualidade. Mostrar “vendas de hoje” sem informar que a fonte parou de atualizar ontem cria uma confiança indevida.

### 2. Python prepara a informação

O código lê os dados e executa as regras necessárias. Ele pode somar valores, agrupar pedidos por região, calcular uma taxa ou separar registros pendentes.

Essa transformação precisa ser verificável. Se “pedido concluído” tiver significados diferentes para as áreas financeira e comercial, a equipe deve definir qual regra a aplicação usará antes de programá-la.

### 3. Streamlit monta a interface

Streamlit recebe textos, valores e tabelas produzidos pelo código e os mostra por meio de componentes.

Um componente interativo também é chamado de widget. Um seletor de período, uma caixa de texto e um botão são widgets. Eles recebem uma escolha e permitem que o código responda a ela.

### 4. A pessoa interage com o resultado

A pessoa escolhe um filtro, lê um indicador, observa um gráfico ou consulta uma tabela. A aplicação recalcula o que for necessário e atualiza a interface.

Essa interação deve ter limites claros. Se um filtro não pode combinar determinados períodos, a tela precisa orientar a pessoa. Se não houver dados, deve dizer que a consulta funcionou, mas não encontrou registros. Uma tela vazia não explica o que aconteceu.

[[visual:fluxo-introdutorio-streamlit]]

## Os principais elementos de uma aplicação

Não é preciso conhecer toda a biblioteca para entender a estrutura de uma aplicação inicial. Alguns elementos aparecem com frequência.

### Textos e orientações

Títulos, subtítulos e textos explicam o objetivo da tela, o período analisado e o significado dos indicadores.

Uma aplicação que mostra “Taxa: 18%” sem dizer taxa de quê obriga a pessoa a adivinhar. “Pedidos entregues com atraso no período: 18%” oferece contexto melhor.

### Filtros e formulários

Filtros permitem escolher um recorte. Período, região, canal de venda e situação do pedido são exemplos.

Quando várias escolhas precisam ser aplicadas juntas, um formulário pode agrupá-las. A pessoa escolhe o período e a região e depois confirma. Isso evita recalcular a tela a cada pequena alteração.

### Indicadores

Indicador é um valor usado para acompanhar uma situação. Total vendido, quantidade de pedidos e tempo médio de atendimento são exemplos.

Todo indicador precisa de nome, unidade, período e definição. R$ 18.500 pode ser faturamento emitido, pagamento recebido ou valor de pedidos criados. A diferença muda a interpretação.

### Tabelas e gráficos

Uma tabela ajuda a conferir detalhes. Um gráfico ajuda a perceber tendência, comparação ou distribuição.

O gráfico não substitui a explicação. Use título, rótulos, unidade e um resumo em texto quando a informação principal não puder depender apenas da imagem ou da cor.

### Mensagens de estado

A aplicação também precisa explicar situações fora do cenário ideal:

- carregando dados;
- nenhum registro encontrado;
- falha ao consultar a fonte;
- dados desatualizados;
- operação concluída.

Esses estados fazem parte da experiência. A pessoa precisa distinguir “não houve vendas” de “não foi possível consultar as vendas”.

## Exemplo realista: acompanhamento de pedidos

Imagine uma loja que recebe pedidos pelo site e pelo WhatsApp. A equipe quer saber quantos pedidos estão aguardando pagamento, separação ou envio.

Uma aplicação introdutória pode começar com uma única pergunta: **quais pedidos precisam de atenção hoje?**

O fluxo seria simples:

1. consultar a lista de pedidos;
2. identificar o status de cada um;
3. calcular a quantidade por status;
4. mostrar os totais;
5. permitir a consulta dos pedidos pendentes.

A tela poderia apresentar a data e a hora da última atualização, três indicadores e uma tabela. Um filtro permitiria escolher o canal de origem.

Se a equipe selecionar WhatsApp, o código filtra os registros e atualiza os resultados. Se a fonte estiver indisponível, a interface informa a falha e não apresenta números antigos como se fossem atuais.

Esse exemplo é realista, mas continua hipotético. Antes de desenvolver, a empresa precisaria definir o que significa “aguardando”, como pedidos duplicados são tratados, quais pessoas podem ver dados de clientes e qual sistema é a fonte oficial.

O ponto principal é que Streamlit organiza a interface. Ele não decide sozinho as regras de negócio, não corrige cadastros e não substitui o controle de acesso.

## O que Streamlit não resolve sozinho?

Uma ferramenta útil também tem limites. Conhecê-los evita tratar um protótipo como solução completa.

### Qualidade dos dados

Se a fonte contém valores ausentes, duplicados ou incorretos, a aplicação precisa tratar ou sinalizar o problema. Uma interface bonita pode tornar um número errado mais convincente, não mais correto.

### Segurança e permissões

Esconder um botão não define quem pode acessar um dado. Autenticação confirma quem é a pessoa; autorização define o que ela pode consultar ou fazer.

Credenciais de banco e chaves de serviços não devem aparecer no código publicado, na tela ou em mensagens de erro. O ambiente precisa armazená-las com segurança.

### Persistência

Algumas escolhas podem ser mantidas durante a sessão da pessoa. Isso não transforma a sessão em banco de dados.

Se uma aprovação, comentário ou correção precisa existir depois que a página for fechada, a aplicação deve gravá-la em um armazenamento persistente, com regras adequadas.

### Desempenho

Uma consulta pequena pode funcionar bem no teste e ficar lenta com muitos dados ou usuários. Antes de tentar acelerar tudo, descubra onde está a demora.

O cache pode reutilizar temporariamente um resultado e evitar trabalho repetido. Ele precisa ter validade clara. Um total guardado por horas pode ser inadequado para uma operação atualizada a cada poucos minutos.

### Operação e manutenção

Colocar a aplicação no ar não encerra o trabalho. É necessário acompanhar erros, atualização dos dados, disponibilidade, backups das fontes e mudanças nas dependências.

Quanto mais crítica for a decisão apoiada, maior deve ser o cuidado com testes, suporte, segurança e recuperação.

## O que fazer com isso?

Se você identificou uma análise repetitiva, não comece tentando criar um sistema inteiro. Escolha uma pergunta pequena que possa ser verificada.

Use este roteiro:

1. **Defina a pergunta.** Exemplo: “quais pedidos estão aguardando envio há mais de um dia?”.
2. **Confirme a fonte.** Saiba onde o status e a data estão registrados.
3. **Escreva a regra.** Defina o que conta como aguardando e como o prazo é calculado.
4. **Escolha o público.** Identifique quem usará a tela e o que essa pessoa pode fazer.
5. **Desenhe uma tela pequena.** Um filtro, poucos indicadores e uma tabela podem bastar.
6. **Valide os números.** Compare o resultado com uma amostra conhecida.
7. **Observe o uso.** Veja se a pessoa entende o resultado e consegue agir.
8. **Registre os limites.** Informe atualização, fonte, ausência de dados e falhas.

Depois do piloto, avalie se Streamlit continua adequado. O próximo artigo, [Quando usar Streamlit?](/blog/streamlit-quando-usar-para-transformar-dados-em-uma-aplicacao-util/), aprofunda critérios como cache, estado de sessão, acesso a bancos, autorização e operação recorrente.

## Perguntas frequentes

### Preciso saber programar para usar uma aplicação Streamlit?

Para usar uma aplicação pronta, geralmente não. A interação acontece no navegador. Para criar e manter a aplicação, é necessário conhecimento de Python e dos dados envolvidos.

### Streamlit serve apenas para dashboards?

Não. Ele pode criar painéis, protótipos, ferramentas internas, demonstrações de modelos e outras aplicações interativas. O uso deve começar pela tarefa ou pergunta, não pelo tipo de gráfico.

### Posso conectar Streamlit a uma planilha ou banco de dados?

Sim, desde que o código use uma integração adequada e trate acesso, falhas e credenciais com segurança. A disponibilidade de uma conexão não garante que todos os dados devam ser exibidos.

### Streamlit substitui um sistema completo?

Depende do contexto. Ele pode sustentar aplicações úteis, mas processos transacionais complexos, permissões detalhadas e experiências muito personalizadas podem exigir outra arquitetura. A escolha deve considerar manutenção, segurança, desempenho e equipe.

### Streamlit corrige dados errados?

Não. O código pode aplicar regras de limpeza conhecidas, mas a equipe ainda precisa identificar a origem do problema e validar o resultado. Uma tela não transforma automaticamente dados ruins em informação confiável.

## Próximo passo

Streamlit aproxima o código Python de quem precisa consultar uma análise. Ele oferece componentes prontos para transformar dados e regras em uma interface interativa.

Comece com uma pergunta, uma fonte e uma ação possível. Explique os indicadores, trate os estados da tela e valide os resultados com quem conhece o processo. A aplicação cresce depois que a primeira versão demonstra utilidade e confiança.

Se sua equipe repete a mesma análise em planilhas ou envia novas imagens a cada pedido de filtro, descreva o fluxo atual. A Koddahub pode ajudar a organizar a pergunta, os dados e um piloto pequeno antes de ampliar a solução.

## Referências

- Streamlit — conceitos fundamentais: https://docs.streamlit.io/get-started/fundamentals/main-concepts
- Streamlit — widgets: https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
- Streamlit — formulários: https://docs.streamlit.io/develop/concepts/architecture/forms
- Streamlit — cache: https://docs.streamlit.io/develop/concepts/architecture/caching
- Streamlit — estado de sessão: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- Streamlit — gerenciamento de segredos: https://docs.streamlit.io/deploy/concepts/secrets
