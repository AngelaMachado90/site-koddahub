---
title: "Extensões de segurança sem excessos"
seo_title: "Extensões de segurança para navegador: como escolher"
meta_description: "Entenda quais extensões de segurança ajudam na navegação, os riscos das permissões e como escolher poucos controles confiáveis e atualizados."
slug: extensoes-seguranca-navegador
category: "Desenvolvimento"
reading_time: 15 minutos
summary: "Extensões podem reforçar senhas, privacidade e bloqueio de conteúdo, mas cada instalação também recebe permissões e amplia a superfície de confiança."
planned_date: 20/09/2026
publish_date: 2026-09-20
status: review
author: VAL — Valor, Autoridade e Linguagem Koddahub
primary_keyword: "extensões de segurança para navegador"
related_terms:
  - "extensões de segurança"
  - "segurança no navegador"
  - "privacidade no navegador"
  - "gerenciador de senhas"
  - "bloqueador de anúncios"
  - "proteção contra phishing"
search_intent: "Informacional"
primary_audience: "Usuários, pequenos empresários, profissionais de tecnologia, desenvolvedores e pessoas que acessam sistemas empresariais pelo navegador"
editorial_objective: "Ensinar a selecionar poucas extensões necessárias, atuais e compatíveis sem tratar quantidade como sinônimo de proteção"
funnel_stage: "Educação e autoridade"
cta_title: "Sua proteção depende de mais que extensões"
cta_text: "A Koddahub pode ajudar sua empresa a organizar ativos, acessos, atualizações e processos antes de escolher novas ferramentas."
cta_label: "Organize os controles"
tags: [Desenvolvimento, Dados, Processos]
reviewed_at: 2026-09-19
review_blockers: [capa definitiva ausente]
cover_brief:
  subject: Mulher profissional utiliza um navegador em notebook ou monitor com poucas extensões organizadas.
  elements: Escudo discreto, senha, privacidade e bloqueio de rastreamento representados sem marcas ou texto na interface.
  style: Ilustração editorial profissional alinhada ao Design System Koddahub, com azul-marinho, azul médio e verde-água.
  avoid: Hacker, capuz, código verde, invasão, malware sensacionalista, excesso de ícones, logotipos e texto legível.
  alt_draft: Mulher profissional analisa no navegador controles de senha, privacidade e bloqueio de rastreamento com poucas extensões organizadas
glossary:
- term: Extensão de navegador
  aliases: [extensão, complemento]
  definition: Programa instalado no navegador para acrescentar ou modificar uma função.
  example: Um gerenciador de senhas preenche credenciais salvas na página de acesso.
  application: Deve ser escolhido conforme necessidade, origem, manutenção e permissões solicitadas.
  related: [Permissão, Superfície de confiança]
- term: Permissão
  aliases: [permissões]
  definition: Autorização concedida a uma extensão para acessar recursos do navegador ou dados de páginas.
  example: Uma extensão pode pedir acesso para ler e alterar dados nos sites visitados.
  application: Deve ser compatível com a função declarada e limitada ao menor acesso necessário.
  related: [Extensão de navegador, Menor privilégio]
- term: Manifest V3
  aliases: [MV3, Manifesto V3]
  definition: Plataforma atual de extensões do Chromium que define APIs, permissões e regras de execução.
  example: Bloqueadores de conteúdo para Chrome precisam trabalhar com os recursos oferecidos pelo Manifest V3.
  application: Afeta compatibilidade e capacidade de algumas extensões, por isso recomendações antigas podem não continuar válidas.
  related: [Chromium, Bloqueador de conteúdo]
- term: Superfície de confiança
  aliases: [dependências confiadas]
  definition: Conjunto de programas, pessoas e serviços que recebem capacidade para influenciar a navegação ou os dados.
  example: Cada extensão instalada acrescenta seu código, fornecedor, atualizações e permissões ao ambiente confiado.
  application: Ajuda a explicar por que instalar mais controles também pode criar novas dependências.
  related: [Extensão de navegador, Cadeia de fornecimento]
- term: Phishing
  aliases: [página de phishing, fraude de identidade]
  definition: Tentativa de imitar uma organização ou pessoa para induzir a vítima a fornecer dados ou executar uma ação.
  example: Uma página parecida com o banco solicita senha e código de autenticação.
  application: Proteções do navegador ajudam a alertar sobre páginas conhecidas, mas não substituem atenção ao endereço e ao pedido recebido.
  related: [Proteção por reputação, Engenharia social]
didactic_visuals:
- id: checklist-extensao
  type: checklist
  title: Oito verificações antes de instalar
  caption: Uma extensão só deve entrar no navegador quando sua função, origem, manutenção e alcance forem compreensíveis.
  alt: Checklist com oito perguntas para avaliar necessidade, manutenção, documentação e permissões de uma extensão.
  data_kind: NÃO SE APLICA
  items:
  - title: Necessidade
    text: Eu consigo explicar qual problema esta extensão resolve?
  - title: Recurso nativo
    text: O navegador já oferece uma proteção adequada para essa necessidade?
  - title: Responsável
    text: Quem desenvolve e publica a extensão?
  - title: Manutenção
    text: A ferramenta continua atualizada e compatível com meu navegador?
  - title: Permissões
    text: O acesso solicitado corresponde à função oferecida?
  - title: Documentação
    text: Existem documentação e canais oficiais verificáveis?
  - title: Dados
    text: Ela precisa ler ou alterar dados em todos os sites?
  - title: Saída
    text: Eu entendo o impacto de remover a extensão amanhã?
- id: categorias-extensoes
  type: table
  title: Escolha pela necessidade
  caption: Os exemplos foram confirmados em fontes oficiais em 19 de setembro de 2026; compatibilidade e políticas podem mudar.
  alt: Tabela relaciona necessidades de navegação a categorias, exemplos atuais e principais cuidados.
  data_kind: NÃO SE APLICA
  headers: [Necessidade, Categoria, Exemplo possível, Cuidado principal]
  rows:
  - ["Criar e preencher senhas únicas", "Gerenciador de senhas", "Bitwarden ou gerenciador integrado verificado", "Proteger a conta principal e evitar dois preenchimentos automáticos concorrentes"]
  - ["Reduzir anúncios e rastreadores", "Bloqueador de conteúdo", "uBlock Origin no Firefox; uBlock Origin Lite ou AdGuard MV3 em Chromium", "Confirmar a versão oficial, a compatibilidade e as permissões"]
  - ["Controlar scripts por site", "Bloqueador de scripts", "NoScript para uso avançado", "Pode quebrar páginas e exige decisões frequentes"]
  - ["Reduzir rastreamento entre sites", "Proteção de privacidade", "Recurso nativo do navegador ou extensão necessária e verificada", "Privacidade não substitui proteção contra malware ou roubo de conta"]
  - ["Receber alertas sobre páginas maliciosas", "Proteção por reputação", "Safe Browsing, proteção do Firefox, SmartScreen ou alerta do Safari", "Verificar primeiro o controle nativo e não confiar cegamente no alerta"]
---
# Extensões de segurança sem excessos

Ao procurar formas de navegar com mais segurança, é comum encontrar listas com dezenas de extensões. Há bloqueadores de anúncios, gerenciadores de senhas, controles de scripts, ferramentas antirrastreamento e complementos que prometem identificar páginas maliciosas. A impressão inicial pode ser que, se uma extensão protege, instalar dez deve proteger ainda mais.

Esse raciocínio ignora o que uma extensão representa. Ela executa código dentro do navegador, recebe determinadas permissões, depende de atualizações e acrescenta um fornecedor à cadeia de confiança. Algumas precisam ler ou alterar partes das páginas visitadas para cumprir sua função. Uma extensão necessária e bem mantida pode reduzir riscos; uma coleção redundante, abandonada ou excessivamente autorizada pode criar novos problemas.

A regra prática deste guia é: instale apenas aquilo cuja função você consegue explicar. Antes de procurar uma marca, defina a necessidade, confira o que o navegador já oferece e avalie se a extensão acrescenta um controle proporcional ao acesso solicitado.

## Antes de instalar: o navegador já possui proteções

Navegadores atuais não começam desprotegidos. Eles recebem atualizações, isolam processos, controlam permissões de sites e incluem mecanismos contra parte das páginas fraudulentas, downloads maliciosos e rastreamento. A configuração exata varia conforme o produto, a versão, o sistema operacional e as escolhas da pessoa ou da organização.

O Chrome oferece Navegação Segura e um gerenciador de senhas capaz de gerar, armazenar e verificar credenciais. O Firefox reúne proteção contra rastreamento, isolamento de cookies, alerta contra páginas enganosas e malware e um modo que prioriza HTTPS. O Edge utiliza o Microsoft Defender SmartScreen para alertar sobre páginas de phishing e downloads maliciosos conhecidos. O Safari inclui prevenção de rastreamento entre sites e aviso sobre páginas fraudulentas.

Esses recursos não tornam qualquer navegação segura, mas mudam a pergunta. Em vez de instalar automaticamente uma extensão “antiphishing”, verifique se a proteção nativa está ativa, atualizada e administrada pela empresa quando aplicável. Duplicar dois controles que consultam reputação semelhante pode aumentar alertas e dependências sem dobrar a segurança.

Comece atualizando o navegador e o sistema operacional, revisando as configurações de proteção e removendo extensões sem uso. Depois identifique a lacuna que permanece. Essa ordem evita instalar um complemento para resolver algo que o próprio navegador já atende de maneira suficiente para aquele contexto.

## 1. Bloqueadores de anúncios e rastreamento

Um bloqueador de conteúdo impede determinadas requisições, elementos ou scripts com base em regras. Isso pode reduzir anúncios, rastreadores e a quantidade de código de terceiros carregado em uma página. A redução é útil para privacidade e também pode diminuir o contato com publicidade maliciosa, mas não transforma todo anúncio em ameaça nem substitui os demais controles do dispositivo.

Publicidade é uma forma de financiar conteúdo; código malicioso é código criado ou comprometido para causar dano. Os dois podem se cruzar quando uma campanha ou cadeia publicitária distribui conteúdo abusivo, situação conhecida como publicidade maliciosa. Um bloqueador reduz parte dessa exposição, porém não avalia todas as ações de uma página e não deve ser tratado como antivírus completo.

Em setembro de 2026, a recomendação precisa considerar o navegador. O projeto oficial informa que o uBlock Origin completo continua disponível no Firefox e que funciona melhor nesse navegador. A versão completa foi removida da Chrome Web Store em 31 de agosto de 2026 com o encerramento do suporte às extensões Manifest V2. Portanto, uma lista que manda instalar o mesmo uBlock Origin no Chrome e no Firefox está desatualizada.

Para navegadores baseados em Chromium, o mesmo desenvolvedor mantém o uBlock Origin Lite, construído sobre as APIs do Manifest V3. “Lite” não é apenas outro nome para o produto original: a arquitetura e as capacidades disponíveis são diferentes. A escolha deve partir da versão oficial compatível, e não de cópias com nome parecido encontradas na loja.

O AdGuard também mantém uma extensão de navegador com versões adaptadas ao Manifest V3, além de publicação para Firefox. Ele é um exemplo possível, não uma classificação de “melhor”. Em qualquer caso, confirme o responsável oficial, a loja correta, a versão atual, as permissões e a documentação. Não combine vários bloqueadores esperando proteção adicional: regras concorrentes podem dificultar diagnóstico, quebrar páginas e tornar impossível saber qual controle causou um comportamento.

Para a maioria das pessoas, um bloqueador de conteúdo confiável e compatível é mais administrável que uma coleção de bloqueadores sobrepostos. Quando uma página falhar, desative temporariamente apenas no domínio necessário, entenda o efeito e evite criar exceções amplas por conveniência.

## 2. Gerenciadores de senhas

O gerenciador de senhas ocupa uma categoria diferente porque seu benefício principal não vem de bloquear uma página. Ele ajuda a criar e usar uma senha forte e única para cada serviço. Se uma credencial vazar, a reutilização deixa de abrir automaticamente outras contas.

Navegadores já oferecem gerenciadores integrados, e eles podem ser suficientes para muitas pessoas quando a conta principal está protegida, os dispositivos são confiáveis e o processo de recuperação é conhecido. Um gerenciador dedicado pode fazer sentido para quem usa diferentes navegadores e sistemas, precisa compartilhar credenciais empresariais de modo controlado ou deseja recursos administrativos específicos.

O Bitwarden é um exemplo atual de serviço dedicado com extensão oficial. Sua documentação confirma geração de senhas, associação de credenciais a endereços de sites e diferentes formas de preenchimento. O preenchimento automático reduz cópias manuais, mas exige acesso aos campos da página. Essa capacidade explica por que origem e permissões da extensão precisam ser tratadas com seriedade.

Se escolher um gerenciador dedicado, evite deixar o preenchimento do navegador e o da extensão disputando os mesmos campos. A própria documentação do Bitwarden orienta torná-lo o gerenciador padrão e desativar o recurso concorrente quando necessário. Proteja a conta principal com senha exclusiva, autenticação multifator quando suportada e um plano seguro de recuperação.

Preenchimento automático não autoriza agir sem atenção. Antes de confirmar, confira o domínio e o contexto. O gerenciador pode ajudar a não preencher credenciais em um endereço diferente do cadastrado, mas uma página legítima comprometida ou uma decisão incorreta de associação ainda exige análise.

## 3. Bloqueadores de scripts

JavaScript permite que páginas respondam a cliques, validem formulários, atualizem conteúdo, executem aplicações e se comuniquem com serviços. Grande parte da web moderna depende dele. Bloquear scripts reduz a execução de conteúdo ativo não autorizado, mas também pode impedir login, pagamento, vídeo, mapas, menus e ferramentas de trabalho.

O NoScript permanece mantido em 2026 e possui versões oficiais para Firefox e Chromium. Ele permite controlar quais origens podem executar scripts e outros conteúdos. Essa abordagem oferece controle detalhado, mas transfere para a pessoa decisões técnicas frequentes sobre domínios principais, serviços de entrega, autenticação e recursos de terceiros.

Por isso, NoScript não é uma recomendação automática para o usuário comum. Um profissional técnico pode justificar o uso quando compreende o funcionamento das páginas, sabe ler os domínios envolvidos e consegue investigar o que deixou de funcionar. Em um computador de atendimento, instalar o bloqueio sem suporte pode interromper sistemas essenciais e incentivar exceções indiscriminadas.

Quem adotar esse tipo de extensão deve começar com um perfil controlado, testar os sistemas necessários e documentar exceções. Permitir tudo sempre que algo quebra anula o objetivo. Bloquear tudo sem entender o fluxo também não é segurança operacional: pode apenas transferir o risco para atalhos e improvisos.

## 4. Extensões de privacidade

Privacidade e segurança se relacionam, mas não são sinônimos. Privacidade trata do controle sobre coleta, associação e uso de informações. Segurança busca reduzir acesso, alteração, interrupção ou fraude indevidos. Uma extensão pode limitar rastreadores ou cookies sem detectar malware; outra pode alertar sobre phishing sem impedir publicidade comportamental.

Antes de instalar um complemento de privacidade, revise os controles nativos. Firefox e Safari, por exemplo, oferecem mecanismos contra rastreamento entre sites. Chrome e Edge também fornecem configurações relacionadas a cookies, dados de navegação e permissões. A ferramenta adicional precisa resolver uma lacuna concreta, e não apenas repetir um rótulo desejável.

Considere também que uma extensão de privacidade pode precisar observar as páginas justamente para identificar rastreadores. Isso não a torna automaticamente inadequada, mas aumenta a importância de verificar desenvolvedor, política de dados, código ou documentação quando disponível e histórico de manutenção. “Privacidade” no nome não elimina a necessidade de confiança.

Evite promessas absolutas como “navegação anônima”. Bloquear rastreadores conhecidos não impede identificação por login, endereço IP, comportamento, configuração do dispositivo ou informações fornecidas diretamente. A comunicação responsável deve dizer qual mecanismo é reduzido e quais limites permanecem.

## 5. Proteção contra phishing e páginas maliciosas

Chrome, Firefox, Edge e Safari já incluem alertas para determinadas páginas conhecidas como fraudulentas ou maliciosas. Essas proteções usam sinais e reputação disponíveis ao fornecedor. Elas são úteis, mas uma página recém-criada pode ainda não estar catalogada, e uma fraude pode acontecer em um serviço legítimo ou por mensagem antes mesmo de o navegador abrir um endereço.

Uma extensão adicional só faz sentido quando acrescenta uma fonte, política ou integração necessária e compreendida. Em ambiente corporativo, por exemplo, a organização pode adotar filtragem de endereços, proteção de endpoint ou políticas gerenciadas. Essa decisão pertence à arquitetura de segurança da empresa, não a uma instalação individual baseada em uma lista da internet.

Duplicar alertas pode gerar fadiga. Quando diferentes produtos exibem avisos frequentes ou contraditórios, a pessoa aprende a fechá-los sem ler. A qualidade do fluxo importa tanto quanto a quantidade de bloqueios: o alerta deve explicar o risco, oferecer uma saída segura e evitar exceções permanentes feitas sob pressão.

Nenhuma extensão confirma que uma página é legítima apenas porque permaneceu silenciosa. Confira o domínio, desconfie de pedidos urgentes, não reutilize senhas e valide solicitações sensíveis por outro canal. A proteção técnica apoia a decisão humana; não a substitui.

## O risco que quase ninguém lembra: a própria extensão

Extensões têm privilégios diferentes. Algumas acessam apenas uma função específica; outras precisam ler e alterar dados em determinados sites ou em todos eles. O Chrome explica que essa permissão pode permitir acesso ao conteúdo das páginas visitadas. A mensagem de instalação não prova que o complemento seja malicioso, mas revela o alcance que ele terá se apresentar uma falha ou for comprometido.

O risco não termina no dia da instalação. O código recebe atualizações, bibliotecas mudam, contas de publicação podem ser atacadas e um projeto pode trocar de proprietário. Uma extensão popular hoje pode ficar abandonada amanhã. A loja oficial reduz parte do risco ao aplicar processos de revisão e remoção, mas não substitui avaliação nem garante que toda atualização será adequada.

Esse é um problema de cadeia de fornecimento: a navegação passa a depender do desenvolvedor, das dependências usadas no projeto, da conta que publica a extensão e da loja que distribui atualizações. Quanto maior a permissão, maior o impacto possível de uma alteração indevida. O princípio do menor privilégio recomenda conceder somente o acesso necessário à função.

Antes de instalar, verifique quem desenvolve, de onde veio, quais permissões pede, quando recebeu atualização, se existe documentação, qual política de privacidade se aplica e se a necessidade é real. Depois da instalação, revise periodicamente a lista e remova o que não usa. O Google recomenda manter apenas aplicativos e extensões necessários, especialmente em dispositivos com informações sensíveis.

[[visual:checklist-extensao]]

Uma mudança de permissão merece nova análise. Se um bloqueador passa a pedir acesso sem relação clara com sua função, não confirme mecanicamente. Leia as notas da versão e a documentação oficial. Em computadores corporativos, encaminhe a decisão à pessoa responsável em vez de contornar a política.

## Cinco extensões fazem mais sentido que vinte?

Não existe um número universal. A regra útil é “menos, mas melhores”: cada extensão deve ter função conhecida, origem verificável, manutenção ativa e permissões proporcionais. Duas extensões bem escolhidas podem atender uma pessoa, enquanto uma função técnica específica pode justificar outra combinação.

Para um usuário comum, o conjunto pode se limitar ao gerenciador de senhas escolhido, às proteções nativas do navegador e, se houver necessidade, a um bloqueador de conteúdo compatível. Instalar controle avançado de scripts sem compreender suas decisões pode criar mais interrupções do que benefício.

Um profissional técnico pode usar NoScript ou configurações avançadas de bloqueio porque consegue investigar recursos, separar domínios e manter exceções. Isso não torna a configuração adequada para colegas que dependem de sistemas web e precisam de comportamento previsível.

Em ambiente corporativo, a escolha não deve ficar inteiramente com cada pessoa. A organização pode definir uma lista permitida, instalar extensões por política e revisar atualizações. Essa gestão reduz variações, melhora o suporte e permite revogar rapidamente uma extensão problemática. A decisão considera os dados acessados, não apenas a preferência individual.

## Então, quais extensões instalar?

Comece pela necessidade, não por um ranking. Uma tabela não consegue escolher pela pessoa, mas ajuda a separar categorias e cuidados.

[[visual:categorias-extensoes]]

Os exemplos não são selos permanentes. Compatibilidade, disponibilidade, propriedade, políticas e manutenção podem mudar. Confirme a fonte oficial e as condições atuais no momento da instalação. Em especial, não siga instruções antigas para instalar manualmente uma versão completa do uBlock Origin no Chrome: instalações fora da loja exigem atualização manual e ampliam a responsabilidade da pessoa.

Também não procure uma extensão para substituir atualização do navegador, autenticação multifator, proteção do dispositivo, cópias de segurança ou orientação contra fraude. Esses controles atuam em partes diferentes do risco. O navegador é apenas uma das portas usadas para acessar informações e sistemas.

## Segurança não é uma coleção de ícones

Uma configuração responsável começa pelas pessoas que usam o navegador, pelos dados que acessam e pelas tarefas que precisam concluir. A tecnologia deve reduzir risco sem tornar o trabalho incompreensível. A transformação ocorre quando a escolha vira um processo: necessidade registrada, origem verificada, permissão analisada, implantação controlada e revisão periódica.

Extensões de segurança para navegador podem ajudar, mas não resolvem sozinhas a segurança de uma empresa. Inventário de ativos, controle de acesso, atualizações, autenticação, backups, monitoramento e resposta a incidentes continuam necessários. O melhor complemento é aquele que resolve uma lacuna real e permanece administrável.

Se sua empresa precisa organizar essas decisões, o primeiro passo não é instalar outra extensão. É identificar quais navegadores, contas, sistemas e dados existem e definir quais controles precisam ser padronizados. A Koddahub pode ajudar a transformar esse diagnóstico em prioridades adequadas à operação.

## Perguntas frequentes

### Extensões de navegador são seguras?

Elas podem ser usadas com segurança, mas não são confiáveis apenas por estarem em uma loja. Avalie desenvolvedor, origem, manutenção, permissões, documentação e necessidade. Remova extensões abandonadas ou que não são mais utilizadas.

### Quanto menos extensões, melhor?

Menos extensões reduzem dependências e facilitam manutenção, mas quantidade não é o único critério. Uma extensão necessária e bem administrada pode oferecer benefício real. O objetivo é manter apenas controles justificáveis, não chegar a um número arbitrário.

### Um bloqueador de anúncios aumenta a segurança?

Ele pode reduzir o carregamento de anúncios, rastreadores e parte do conteúdo de terceiros, diminuindo algumas exposições. Isso não garante proteção contra malware, phishing, roubo de conta ou falhas do sistema. Deve ser uma camada, não a única defesa.

### Preciso de uma extensão antivírus no navegador?

Não necessariamente. Primeiro verifique as proteções do navegador, do sistema operacional e da solução de segurança já adotada. Uma extensão adicional só deve ser instalada se acrescentar uma função clara, compatível e não redundante.

### O gerenciador de senhas do navegador é suficiente?

Pode ser suficiente para algumas pessoas. A decisão depende de dispositivos, compartilhamento empresarial, administração, recuperação e integração entre navegadores. Mais importante que a marca é usar senhas únicas, proteger a conta principal e manter um processo de recuperação seguro.

### Uma extensão pode ler meus dados?

Depende das permissões. Algumas podem ler ou alterar dados nos sites autorizados, ver endereços visitados ou interagir com abas. O navegador mostra avisos de permissão; leia-os e confirme se o alcance corresponde à função.

## Links internos sugeridos

- /blog/ferramentas-gratuitas-ciberseguranca/
- /blog/e-seguro-usar-claude/

## Referências para revisão

Google Chrome, permissões solicitadas por extensões: https://support.google.com/chrome_webstore/answer/186213

Google Chrome, instalação e controle de acesso das extensões aos sites: https://support.google.com/chrome/answer/2664769

Google Chrome, orientação para remover extensões desnecessárias e usar senhas únicas: https://support.google.com/chrome/answer/46526

Mozilla, recursos de privacidade e segurança do Firefox: https://support.mozilla.org/en-US/kb/firefox-privacy-and-security-features

Microsoft, navegação segura e Microsoft Defender SmartScreen no Edge: https://support.microsoft.com/en-us/edge/securely-browse-the-web-in-microsoft-edge

Apple, prevenção de rastreamento entre sites no Safari: https://support.apple.com/guide/safari/prevent-cross-site-tracking-sfri40732/mac

Apple, configurações de segurança e alerta de site fraudulento no Safari: https://support.apple.com/guide/safari/ibrw1074/mac

uBlock Origin, projeto oficial, compatibilidade e situação no Chrome Web Store: https://github.com/gorhill/uBlock/

uBlock Origin Lite, versões atuais e compatibilidade: https://github.com/uBlockOrigin/uBOL-home/releases

AdGuard Browser Extension, projeto oficial e versões atuais: https://github.com/AdguardTeam/AdguardBrowserExtension

Bitwarden, preenchimento pelo complemento do navegador: https://bitwarden.com/help/auto-fill-browser/

Bitwarden, geração de senhas: https://bitwarden.com/help/generator/

NoScript, versões oficiais e compatibilidade atual: https://www.noscript.net/getit/

CISA, proteção de navegadores e defesa contra publicidade maliciosa: https://www.cisa.gov/sites/default/files/publications/Capacity_Enhancement_Guide-Securing_Web_Browsers_and_Defending_Against_Malvertising_for_Federal_Agencies.pdf
