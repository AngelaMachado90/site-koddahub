---
title: "O que é RPA?"
seo_title: "O que é RPA? Entenda a automação de tarefas | Koddahub"
meta_description: 'RPA é a automação de tarefas repetitivas em interfaces de sistemas. Entenda como funciona, veja um exemplo simples e saiba quando escolher outra abordagem.'
slug: descomplicando-a-ti-o-que-e-rpa
category: "Automação"
series: '#DescomplicandoATI'
reading_time: 15 minutos
modified_date: 2026-09-15
summary: 'RPA automatiza tarefas repetitivas em telas de sistemas. Veja um exemplo, os limites e as perguntas que ajudam a decidir se vale usar.'
planned_date: 13/09/2026
publish_date: 2026-09-13
originally_published_date: 2026-09-14
status: published
author: VAL — Valor, Autoridade e Linguagem Koddahub
cover: /assets/images/blog/descomplicando-ti-rpa.webp
cover_alt: Robô de software ilustrado transfere cartões de dados entre duas interfaces, com uma pessoa acompanhando a tarefa
cover_width: 1672
cover_height: 941
image_source:
  provider: OpenAI
  type: imagem gerada para o Blog Koddahub
cta_title: "Quer saber se uma tarefa combina com RPA?"
cta_text: "A Koddahub ajuda a separar tarefas repetitivas de processos que ainda precisam ser simplificados."
cta_label: "Avalie seu processo"
tags: [RPA, Automação, Processos]
glossary:
- term: RPA
  aliases:
  - automação robótica de processos
  definition: Tecnologia que repete ações humanas em telas seguindo regras definidas.
  example: Um robô copia dados de pedidos de uma planilha para um sistema.
  application: Ajuda em tarefas repetitivas quando não existe uma integração direta adequada.
  related:
  - Bot
  - Automação
  - Processo
- term: Bot
  aliases:
  - robô de software
  - robô
  definition: Programa que executa ações automaticamente conforme instruções.
  example: O bot abre um relatório, confere campos e salva o arquivo.
  application: Executa partes previsíveis de um processo sem substituir decisões humanas complexas.
  related:
  - RPA
  - Automação
- term: Automação
  aliases:
  - automatizar
  definition: Uso de regras e tecnologia para executar uma tarefa com menos intervenção manual.
  example: Enviar uma confirmação após o recebimento de um formulário.
  application: Reduz trabalho repetitivo quando entradas, regras e resultados são conhecidos.
  related:
  - RPA
  - Processo
- term: Processo
  aliases:
  - processos
  definition: Sequência de atividades usada para chegar a um resultado.
  example: Receber um pedido, validar o pagamento e separar o produto.
  application: Mostra o que precisa ser entendido antes de escolher uma automação.
  related:
  - Automação
  - RPA
didactic_visuals:
- id: rpa-manual-automatico
  type: comparison
  title: Tarefa manual e tarefa com RPA
  caption: O RPA assume passos repetitivos e baseados em regras; exceções e decisões continuam precisando de tratamento
    definido.
  alt: Comparação entre uma pessoa repetindo ações em telas e um robô executando as mesmas regras.
  data_kind: NÃO SE APLICA
  items:
  - title: Execução manual
    text: A pessoa abre telas, copia campos e confere cada registro.
  - title: Execução com RPA
    text: O robô repete os passos previstos e encaminha exceções para uma pessoa.
---
# O que é RPA?

**#DescomplicandoATI.** Sabe aquele termo da área de TI que você tem medo de perguntar para não parecer burro? Pode perguntar. Nesta série, a ideia é explicar a tecnologia sem pressupor que todo mundo já conhece as siglas. Começamos por RPA.

## O que é?

RPA é a sigla de **Robotic Process Automation**, ou automação robótica de processos. O “robô” normalmente é um software que executa uma sequência de ações em interfaces: abrir um programa, localizar um campo, copiar uma informação, preencher um formulário, clicar em um botão e conferir a resposta. Não é um robô físico andando pelo escritório. A palavra “processos” também merece cuidado: a ferramenta executa etapas definidas; ela não decide sozinha qual processo da empresa faz sentido.

### RPA assistida e não assistida


Na **RPA assistida**, uma pessoa inicia ou acompanha a automação enquanto trabalha. É útil quando há decisão humana no meio da tarefa: o software prepara informações, e a pessoa confirma o próximo passo. Na **RPA não assistida**, a execução ocorre sem alguém operando a tela naquele momento, por exemplo em um horário programado. Nesse caso, monitoramento, credenciais, tratamento de falhas e capacidade de intervenção ficam ainda mais importantes.

“Não assistida” não quer dizer “sem responsável”. Alguém deve saber quando o fluxo falhou, qual pedido ficou pendente e como retomar com segurança. O nível de supervisão é uma decisão de operação, não uma promessa de autonomia total.

[[visual:rpa-manual-automatico]]

## Exemplo simples


Imagine uma pessoa que recebe uma planilha com pedidos aprovados e precisa cadastrá-los em um sistema antigo. Para cada linha, ela abre a tela, procura o cliente, preenche campos, salva e anota o número gerado. Se as regras forem estáveis e a tarefa acontecer muitas vezes, um fluxo de RPA pode repetir esses passos na interface.

O exemplo não significa que qualquer planilha deva virar automação. Primeiro é preciso confirmar a origem dos pedidos, os campos obrigatórios, as regras para duplicidade e o que fazer quando o cliente não é encontrado. Se um pedido exigir julgamento humano, o fluxo deve parar e encaminhar o caso. Automatizar cliques sem entender essas situações apenas acelera erros.


## Por que importa?

RPA importa porque tarefas repetitivas executadas em sistemas sem integração consomem tempo, aumentam o risco de digitação incorreta e dificultam manter um padrão. Quando o processo é adequado, o software assume a repetição e deixa as exceções e decisões com as pessoas. O benefício depende de escolher bem a tarefa e acompanhar o resultado; automatizar um processo confuso apenas repete a confusão mais rápido.

### RPA, API, workflow e inteligência artificial


Uma API permite que sistemas troquem dados por uma interface técnica definida para isso. Quando uma API adequada existe e atende à necessidade, ela costuma ser uma opção mais direta do que automatizar a tela que uma pessoa usa. O RPA ganha relevância quando a tarefa depende de uma aplicação sem integração disponível, de um sistema legado ou de uma etapa que só pode ser executada pela interface autorizada.

Uma plataforma de workflows, como n8n, pode orquestrar chamadas a APIs, regras e notificações. Ela não é sinônimo de RPA de desktop. Em uma solução maior, as abordagens podem se complementar: uma integração recebe o pedido, um robô executa uma etapa em sistema legado, e outra integração comunica o resultado. A arquitetura depende das capacidades reais dos sistemas e da segurança exigida.

RPA também não é inteligência artificial. Um fluxo tradicional segue regras e passos definidos. Recursos de IA podem apoiar classificação ou leitura de documentos em alguns projetos, mas isso adiciona incerteza e necessidade de validação. Para copiar um identificador de um campo para outro, não é preciso inventar uma decisão inteligente.


### Quando vale considerar RPA?


Faça estas perguntas antes de escolher a ferramenta:

1. **A tarefa é repetitiva e tem regras claras?** Descreva uma ocorrência completa, com entrada e resultado esperado.
2. **Há volume ou frequência suficientes?** A economia de trabalho precisa compensar implantação, testes e manutenção.
3. **Existe API ou outra integração melhor?** Compare estabilidade, permissões e custo de operação.
4. **As telas são razoavelmente estáveis?** Mudanças frequentes podem tornar o fluxo frágil.
5. **Quem resolve exceções?** Dados ausentes, duplicados e indisponibilidade precisam de saída definida.
6. **Como comprovar o resultado?** Registre o que foi processado, o que falhou e o que precisa de revisão.

Para um processo raro, ainda em mudança ou cheio de decisões subjetivas, um formulário melhor, uma regra mais clara ou uma integração simples podem ser mais úteis. O RPA não deve esconder um problema de processo.


## Como funciona?


Ferramentas de RPA podem identificar elementos da interface, como campos e botões, e executar ações sobre eles. Em algumas situações usam seletores de elementos; em outras, reconhecimento de imagem ou coordenadas. A escolha afeta a confiabilidade. Se o sistema muda um rótulo, reorganiza a tela ou exibe uma janela inesperada, o robô pode não encontrar o próximo passo.

Por isso, um bom fluxo não é só uma gravação de cliques. Ele verifica se a tela esperada abriu, se o dado foi aceito e se o resultado foi salvo. Também registra a falha de forma compreensível e permite retomar ou revisar a tarefa sem cadastrar o mesmo pedido duas vezes. A equipe precisa testar o fluxo no ambiente e na conta em que ele realmente executará.


### Mapeie o trabalho antes de gravar a primeira ação


O início de um projeto de RPA não é abrir a ferramenta. É acompanhar o trabalho real. Peça que uma pessoa execute alguns casos normais e alguns casos difíceis, explicando por que escolheu cada caminho. Anote entradas, sistemas envolvidos, decisões, saídas e evidências de conclusão. Depois compare essa descrição com o procedimento escrito: muitas exceções vivem apenas na experiência de quem opera a tarefa.

No exemplo dos pedidos, o caminho normal começa com uma linha válida na planilha e termina com um identificador gerado no sistema. Mas o que acontece se o cliente tem dois cadastros? Se o preço mudou depois da aprovação? Se a tela salvou e a conexão caiu antes de mostrar a confirmação? Se a planilha for reenviada? Cada situação muda a definição de sucesso. O fluxo precisa saber quando continuar, quando tentar novamente e quando pedir avaliação humana.

Uma regra útil é separar três estados: concluído e verificado; pendente para nova tentativa segura; e bloqueado para revisão. “Deu erro” é pouco informativo. A equipe precisa saber qual pedido ficou em cada estado e o que deve fazer em seguida. Essa classificação também evita que uma falha temporária seja confundida com uma rejeição de negócio.

Ao mapear, procure oportunidades de simplificar antes de automatizar. Talvez a planilha contenha colunas que ninguém usa, ou o cadastro exija copiar um dado que já existe em outro sistema. Eliminar um passo desnecessário é mais barato de manter que ensinar um robô a repeti-lo. O desenho final deve refletir o processo que a equipe quer operar, não apenas uma fotografia de hábitos antigos.


### Segurança e operação fazem parte da solução


O robô pode ter acesso a sistemas e dados sensíveis. Use uma conta com as permissões necessárias, guarde credenciais fora do código e limite quem pode iniciar, alterar e consultar as execuções. Evite registrar senhas ou dados pessoais em capturas e logs. Se o sistema exigir autenticação em duas etapas ou interação humana, trate isso como requisito do desenho; não tente contorná-lo.

Também combine uma rotina de manutenção. Atualizações de navegador, sistema ou aplicação podem afetar a automação. Indicadores úteis incluem tarefas concluídas, falhas por motivo, tempo de execução e casos enviados para revisão. Uma automação que “terminou sem erro” mas não salvou o pedido não cumpriu sua função.


## Exemplo real

O cenário a seguir é um exemplo hipotético construído a partir de situações comuns de operação. Ele mostra como o fluxo pode ser desenhado e validado, sem representar dados ou resultados de uma empresa específica.


Para tornar a ideia concreta, imagine um piloto com dez pedidos autorizados. O fluxo lê um pedido, verifica se os campos obrigatórios estão presentes e procura o identificador no sistema de destino. Se já existe um registro correspondente, não cria outro: registra a ocorrência e segue a regra de revisão. Se não existe, preenche a tela, confere os valores visíveis, salva e procura o número do novo cadastro.

O número exibido é uma evidência, mas a confirmação ideal depende do sistema. Pode ser necessário abrir o registro salvo e comparar campos importantes. Se a aplicação não permite essa verificação, trate essa limitação como risco operacional. Uma automação que clica em “salvar” e marca sucesso sem conferir o resultado está medindo a própria atividade, não a entrega.

Depois de cada pedido, o fluxo registra apenas informações necessárias para acompanhar a operação: identificador de origem, estado, horário, motivo de falha quando houver e referência do registro criado. Não coloque senha, dados pessoais desnecessários ou capturas completas em logs. O registro deve ajudar alguém a corrigir um problema sem criar outro problema de privacidade.

No fim do lote, uma pessoa confere quantos pedidos foram concluídos, quantos exigem revisão e se o total corresponde à entrada. Essa reconciliação é importante quando uma execução é interrompida no meio. Se a primeira tentativa processou seis de dez pedidos, a segunda não pode cadastrar os mesmos seis novamente. Essa capacidade de retomar sem duplicar efeitos precisa ser pensada antes do uso recorrente.


### Como testar sem confiar no primeiro caminho feliz


Um teste que cadastra um pedido perfeito mostra apenas que o fluxo consegue seguir o caminho esperado naquele momento. Para avaliar a confiabilidade, prepare casos com campo vazio, cliente inexistente, registro duplicado, formato inválido e tela que demora a carregar. Teste também uma interrupção após o clique em salvar: o robô deve descobrir se o pedido foi criado antes de repetir a ação.

Compare cada resultado com a regra de negócio escrita. O resultado esperado de um caso inválido pode ser “não cadastrar e enviar para revisão”, não “terminar sem erro”. Registre o que foi testado, qual dado de exemplo foi usado, qual saída ocorreu e quem aceitou o comportamento. Use ambiente e dados autorizados; um teste em produção pode criar registros reais e confundir a operação.

Uma mudança de interface merece reteste. Atualizar um seletor até o robô voltar a clicar não basta se o significado do campo mudou. Verifique se o valor foi para o destino correto e se a regra de negócio continua válida. Quando a equipe responsável pelo sistema avisa sobre uma nova versão, combine uma janela para testar o fluxo antes de depender dela.

O piloto deve ter critérios de aceitação proporcionais à tarefa. Por exemplo: todos os casos válidos do conjunto de teste aparecem uma vez no destino; os inválidos não são cadastrados; falhas deixam mensagem compreensível; e uma nova execução não duplica registros já confirmados. Esses critérios são mais úteis que a impressão de que o robô “parece rápido”.


## O que fazer com isso?


Escolha uma tarefa pequena e bem delimitada. Mapeie o caminho normal e três exceções reais. Teste com dados autorizados, compare o resultado com o trabalho manual e defina quem responderá às falhas. Só depois amplie o volume. O objetivo é reduzir trabalho repetitivo mantendo controle sobre o resultado.

Se a sigla RPA já apareceu em uma reunião e agora faz mais sentido, a série cumpriu seu papel. Na próxima vez que alguém sugerir “colocar um robô”, pergunte qual tarefa será feita, por que a interface precisa ser usada e como saberemos que deu certo.


### Avalie custo e benefício incluindo manutenção


Para decidir se RPA vale o esforço, estime o tempo gasto hoje na tarefa e a frequência com que ela acontece. Depois inclua desenho, licença se aplicável, ambiente de execução, testes, suporte e manutenção de seletores. Uma tarefa que economiza alguns minutos por mês pode não compensar um fluxo que exige revisão toda vez que a aplicação muda. Já uma tarefa frequente, estável e verificável pode justificar o investimento.

Não use uma promessa genérica de retorno sobre investimento. Meça um pequeno período real: quantos casos passaram pelo fluxo, quantos exigiram intervenção, quanto tempo a equipe gastou com exceções e quantos erros precisaram de correção. Compare com o processo anterior sob condições semelhantes. Se o volume variou ou as regras mudaram no meio do teste, registre o contexto em vez de atribuir toda diferença à automação.

O custo de falha também importa. Duplicar um pedido pode gerar retrabalho; lançar um valor errado pode afetar um cliente. Quanto maior o impacto de uma ação incorreta, mais forte deve ser a verificação antes e depois dela. Em alguns processos, a melhor escolha é automatizar a preparação e manter a confirmação final com uma pessoa.


### Defina quem cuida do robô depois do piloto


Defina uma pessoa responsável pelo processo e outra pela manutenção técnica, mesmo que em uma equipe pequena esses papéis se encontrem. A primeira sabe qual resultado é correto; a segunda investiga execução, ambiente e integração. Quando o fluxo falha, ambas precisam de um caminho claro para decidir se o caso deve ser reprocessado, corrigido manualmente ou suspenso.

Documente entradas, regras, exceções, permissões, versão do sistema, forma de iniciar e forma de interromper. Registre a última revisão do fluxo e um contato operacional. Um vídeo de gravação pode ajudar no treinamento, mas não substitui instruções sobre o que fazer quando algo sai do esperado.

Monitore resultados de negócio e sinais técnicos. Taxa de casos concluídos, duplicidades evitadas, tempo de tratamento de exceções e volume pendente mostram se a operação funciona. Falhas de autenticação, mudança de tela e indisponibilidade mostram por que ela parou. Olhar apenas a mensagem “execução concluída” deixa o problema invisível.

Quando a automação não for mais útil, desative-a de forma controlada. Revise agendamentos, contas e permissões; preserve registros necessários para a operação e informe quem receberá os casos. Um robô esquecido com acesso ativo a sistemas continua sendo uma responsabilidade, mesmo sem gerar valor.


### Perguntas frequentes


**RPA é um robô físico?**

Não. Em geral é um software que executa etapas em aplicações, muitas vezes interagindo com telas como uma pessoa faria.

**RPA substitui toda a equipe?**

Não. Ela automatiza tarefas delimitadas. Pessoas continuam necessárias para definir regras, tratar exceções, supervisionar resultados e melhorar o processo.

**Toda automação é RPA?**

Não. Uma chamada de API, um script e um workflow também automatizam trabalho, mas usam mecanismos diferentes. A escolha depende da tarefa e dos sistemas disponíveis.

**É possível começar com um processo pequeno?**

Sim. Um piloto com entrada clara, resultado verificável e exceções conhecidas permite avaliar a utilidade antes de ampliar a operação.


## Referências


- Microsoft Learn — introdução aos fluxos de desktop: https://learn.microsoft.com/en-us/power-automate/desktop-flows/introduction
- Microsoft Learn — modos de execução não assistida: https://learn.microsoft.com/en-us/power-automate/desktop-flows/run-unattended-desktop-flows
- Microsoft Learn — elementos de interface e seletores: https://learn.microsoft.com/en-us/power-automate/desktop-flows/ui-elements
- Microsoft Learn — investigação de falhas de execução: https://learn.microsoft.com/en-us/power-automate/desktop-flows/how-to/troubleshoot-unattended-execution-failures
