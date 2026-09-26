---
title: "6 ferramentas gratuitas de cibersegurança"
seo_title: "Ferramentas gratuitas de cibersegurança: 6 opções"
meta_description: "Conheça seis ferramentas gratuitas de cibersegurança, quando usá-las, seus limites e os cuidados necessários para não expor dados."
slug: ferramentas-gratuitas-ciberseguranca
category: "Desenvolvimento"
reading_time: 15 minutos
summary: "Seis serviços ajudam a investigar sinais de segurança, desde que a pergunta venha antes da ferramenta e os dados enviados sejam protegidos."
planned_date: 19/09/2026
publish_date: 2026-09-19
status: scheduled
author: VAL — Valor, Autoridade e Linguagem Koddahub
cover: /assets/images/blog/ferramentas-gratuitas-ciberseguranca.webp
cover_alt: Duas pessoas analisam em uma tela verificações defensivas de e-mail, arquivo, URL, site, endereço IP e servidor
cover_width: 1672
cover_height: 941
image_source:
  provider: OpenAI
  type: imagem gerada para o Blog Koddahub
primary_keyword: "ferramentas gratuitas de cibersegurança"
related_terms:
  - "ferramentas de segurança online"
  - "verificar vazamento de dados"
  - "analisar URL suspeita"
  - "reputação de IP"
  - "segurança digital para pequenas empresas"
search_intent: "Informacional"
primary_audience: "Pequenos empresários, responsáveis por sites, desenvolvedores e equipes de tecnologia sem um time dedicado de segurança"
editorial_objective: "Ensinar a escolher uma ferramenta defensiva pela pergunta, interpretar seus sinais e evitar exposição de dados durante a investigação"
funnel_stage: "Educação e autoridade"
cta_title: "Precisa organizar a segurança antes de escolher ferramentas?"
cta_text: "A Koddahub pode ajudar sua empresa a mapear ativos, entender riscos e priorizar controles compatíveis com a operação."
cta_label: "Organize os próximos passos"
tags: [Dados, Desenvolvimento, Processos]
glossary:
- term: Cabeçalho HTTP
  aliases: [cabeçalhos HTTP]
  definition: Informação enviada entre navegador e servidor para orientar como uma página e seus recursos devem ser tratados.
  example: Um cabeçalho pode determinar que o navegador acesse o site somente por uma conexão HTTPS.
  application: Permite verificar configurações preventivas do site sem representar uma análise completa da aplicação.
  related: [HTTPS, Política de segurança de conteúdo]
- term: Hash
  aliases: [resumo criptográfico, impressão digital do arquivo]
  definition: Código calculado a partir do conteúdo de um arquivo e usado para identificá-lo sem depender de seu nome.
  example: Dois arquivos idênticos produzem o mesmo hash quando calculados pelo mesmo método.
  application: Permite procurar uma análise existente antes de enviar novamente o arquivo a um serviço externo.
  related: [Análise de malware, Indicador]
- term: Reputação de IP
  aliases: [reputação do endereço IP]
  definition: Contexto construído a partir de observações ou relatos anteriores associados a um endereço IP.
  example: Um endereço pode ter sido reportado por tentativas repetidas de acesso a servidores.
  application: Enriquece uma investigação, mas não prova sozinho que uma conexão atual seja maliciosa.
  related: [Endereço IP, Falso positivo]
- term: Falso positivo
  aliases: [detecção incorreta]
  definition: Alerta que classifica como ameaça um conteúdo ou comportamento que, após análise, é legítimo.
  example: Um mecanismo sinaliza um utilitário administrativo conhecido como suspeito.
  application: Mostra por que uma detecção isolada precisa de contexto antes de provocar uma decisão definitiva.
  related: [Análise de malware, Reputação de IP]
- term: Token
  aliases: [token de acesso, código de acesso]
  definition: Valor usado por um sistema para autorizar uma sessão, integração ou ação específica.
  example: Um link de redefinição de senha pode incluir um token temporário na própria URL.
  application: Não deve ser enviado a uma ferramenta pública, pois pode conceder acesso ou revelar informação restrita.
  related: [Credencial, URL]
didactic_visuals:
- id: pergunta-e-ferramenta
  type: table
  title: Comece pela pergunta, não pela ferramenta
  caption: Cada serviço oferece um recorte da investigação; o resultado ainda precisa ser relacionado aos registros e riscos do ambiente.
  alt: Tabela relaciona seis perguntas defensivas às ferramentas adequadas para uma verificação inicial.
  data_kind: NÃO SE APLICA
  headers: [Pergunta inicial, Ferramenta]
  rows:
  - ["Meu e-mail apareceu em vazamentos conhecidos?", "Have I Been Pwned"]
  - ["Quero uma análise inicial de um link ou arquivo não confidencial.", "VirusTotal"]
  - ["Quero verificar configurações HTTP do meu site.", "MDN HTTP Observatory"]
  - ["Esse endereço IP possui histórico de abuso?", "AbuseIPDB"]
  - ["Quais serviços meus estão publicamente visíveis?", "Shodan"]
  - ["Como uma URL pública se comporta ao ser carregada?", "urlscan.io"]
---
# 6 ferramentas gratuitas de cibersegurança

Você recebe um link inesperado por e-mail. Pouco depois, os registros do servidor mostram várias tentativas de acesso. Em outra conversa, alguém pergunta se um endereço corporativo já apareceu em um vazamento. Ou talvez a dúvida seja mais direta: o site utiliza configurações HTTP que ajudam a reduzir riscos conhecidos?

Existem ferramentas gratuitas de cibersegurança que apoiam essas verificações. O problema é que abrir vários serviços, copiar informações e interpretar pontuações sem uma pergunta clara pode gerar mais confusão do que proteção. A investigação também pode criar um risco adicional quando arquivos, endereços internos ou dados pessoais são enviados sem avaliação prévia.

O ponto de partida é simples: primeiro defina a pergunta. Depois escolha a ferramenta. [**Have I Been Pwned**](https://haveibeenpwned.com/), [**VirusTotal**](https://www.virustotal.com/gui/home/upload), [**MDN HTTP Observatory**](https://developer.mozilla.org/en-US/observatory), [**AbuseIPDB**](https://www.abuseipdb.com/), [**Shodan**](https://www.shodan.io/) e [**urlscan.io**](https://urlscan.io/) oferecem sinais úteis para uma análise inicial, mas nenhum deles substitui inventário de ativos, atualização, controle de acesso, cópias de segurança, monitoramento, conscientização e resposta a incidentes.

## Antes de começar: uma ferramenta responde a uma pergunta

Segurança digital não é um botão que classifica uma empresa como segura ou insegura. Cada ferramenta observa uma parte limitada do ambiente. Para usar o resultado com responsabilidade, organize a investigação em quatro elementos: sinal, ferramenta, contexto e decisão.

O sinal é aquilo que chamou a atenção, como um arquivo inesperado, uma URL estranha, um endereço IP recorrente nos registros ou um serviço que parece estar exposto. A ferramenta ajuda a coletar informações adicionais. O contexto relaciona o resultado ao ambiente da empresa. A decisão define o próximo passo, como revisar uma conta, isolar um arquivo, corrigir uma configuração ou encaminhar o caso para análise especializada.

Imagine que um endereço IP recebeu relatos de atividade abusiva. Esse dado não demonstra que toda conexão originada nele seja maliciosa. O endereço pode pertencer a uma rede compartilhada, ter mudado de responsável ou ter sido comprometido anteriormente. Antes de uma medida permanente, a equipe deve conferir seus registros, o horário, o serviço acessado e o comportamento observado.

Essa lógica evita duas armadilhas frequentes. A primeira é transformar um alerta em veredito. A segunda é considerar a ausência de alerta como garantia de segurança. Ferramentas de consulta e scanners trabalham com informações, regras e observações disponíveis naquele momento; sempre haverá aspectos que não foram vistos.

## 1. Have I Been Pwned: exposição em vazamentos conhecidos

O Have I Been Pwned ajuda a responder: “Meu e-mail apareceu em algum vazamento conhecido?”. A consulta pode indicar em quais incidentes catalogados aquele endereço apareceu e quais tipos de dados foram expostos. O resultado ajuda a identificar a necessidade de trocar senhas, revisar credenciais reutilizadas e ativar autenticação multifator, que exige outra forma de confirmação além da senha.

Interprete a ocorrência considerando data e origem. Se o endereço apareceu em um incidente antigo, isso não significa que a conta esteja sendo acessada indevidamente agora. Ainda assim, uma senha que permaneceu em uso ou foi repetida em outros serviços pode continuar oferecendo risco. A medida útil não é entrar em pânico, mas verificar contas relacionadas, encerrar sessões desconhecidas e corrigir hábitos de acesso.

Um resultado sem ocorrências também não comprova que o endereço nunca tenha sido exposto. O próprio serviço explica que ausência de evidência não é evidência de ausência. Podem existir incidentes ainda não descobertos, não divulgados ou não incluídos na base consultada.

Um uso defensivo simples é orientar cada profissional a consultar seu próprio endereço corporativo. Se houver uma ocorrência, a equipe verifica se a senha usada no período foi reutilizada, substitui credenciais quando necessário e revisa os controles da conta. A busca não serve para investigar a vida digital de outras pessoas.

O endereço de e-mail é um dado pessoal. Consultas em escala envolvendo colaboradores, clientes ou terceiros precisam de finalidade, autorização e procedimento definidos. Para a verificação comum, não é necessário fornecer senhas nem outros dados pessoais. Antes de qualquer uso diferente, consulte as condições atuais do serviço.

## 2. VirusTotal: uma segunda análise para arquivos e URLs

O VirusTotal ajuda a responder: “Esse arquivo ou endereço merece uma investigação adicional?”. O serviço reúne resultados de mecanismos de análise, listas de bloqueio e outras fontes. Ao consultar um arquivo ou URL, a pessoa pode observar se diferentes mecanismos encontraram sinais suspeitos e decidir se deve interromper a abertura, isolar o item ou solicitar uma análise mais profunda.

O painel não deve ser lido como votação. Uma detecção isolada pode ser um falso positivo, isto é, algo legítimo classificado incorretamente como ameaça. No sentido oposto, a ausência de detecções não garante que o conteúdo seja seguro. A ameaça pode ser nova, depender de uma condição específica ou não ser reconhecida pelos mecanismos naquele momento.

Há uma precaução importante antes do envio. O VirusTotal informa que resultados básicos de arquivos e URLs submetidos são compartilhados com parceiros de análise. Portanto, a submissão comum não deve ser tratada como um ambiente privado. Primeiro verifique se o arquivo já pode ser consultado por seu hash, um código calculado a partir do conteúdo que funciona como uma impressão digital. Essa pesquisa pode encontrar uma análise existente sem transmitir novamente o arquivo.

Considere um instalador supostamente enviado por um fornecedor. Em vez de executá-lo, confirme a origem por outro canal, verifique a assinatura digital quando houver e pesquise o hash. Se uma submissão for realmente necessária, faça isso somente depois de confirmar que o arquivo não contém informações internas ou confidenciais.

Contratos, planilhas de clientes, documentos pessoais, bancos de dados, credenciais, chaves e tokens não devem ser enviados para uma consulta pública. Se o conteúdo é restrito, a organização precisa de um processo interno ou de uma solução cuja política, configuração e relação contratual tenham sido aprovadas para essa finalidade.

## 3. MDN HTTP Observatory: configurações HTTP do site

O MDN HTTP Observatory ajuda a responder: “Meu site utiliza algumas das principais configurações HTTP de segurança?”. HTTP é o protocolo usado na comunicação entre navegador e servidor. Nessa comunicação, o servidor envia cabeçalhos, informações que orientam o navegador sobre como tratar a página e seus recursos.

Alguns cabeçalhos ajudam a reduzir riscos, como carregamento indevido de conteúdo, abertura do site dentro de páginas de terceiros ou conexões sem a proteção esperada. Ao informar um domínio, o Observatory apresenta nota, testes aprovados ou reprovados e orientações relacionadas. Isso permite identificar configurações ausentes ou inadequadas.

A nota representa apenas esse conjunto de testes. A documentação do Observatory afirma que até uma classificação A+ não comprova que o site inteiro esteja seguro. A ferramenta não demonstra, por exemplo, que a aplicação esteja livre de injeção de SQL, componentes desatualizados, falhas de autenticação, senhas armazenadas incorretamente ou problemas nas regras do sistema.

Também não convém perseguir pontuação sem avaliar o funcionamento real. Uma política de segurança de conteúdo pode exigir adaptação antes de entrar em produção. Copiar uma configuração sem testes pode bloquear scripts, estilos, formulários ou integrações necessárias.

Como exemplo defensivo, o responsável por um site institucional pode executar a consulta no próprio domínio, ler cada recomendação e levar os itens para revisão técnica. Depois das mudanças em um ambiente de teste, deve confirmar que páginas, formulários, pagamentos e integrações continuam funcionando.

Há um detalhe de privacidade: segundo a documentação, qualquer pessoa pode analisar um domínio e o histórico de verificações de cada domínio é público. O serviço é apropriado para sites públicos, mas não deve receber nomes internos cuja divulgação revele detalhes desnecessários da infraestrutura.

## 4. AbuseIPDB: reputação de um endereço IP

O AbuseIPDB ajuda a responder: “Esse endereço IP possui histórico de atividades reportadas como abusivas?”. Um endereço IP identifica um ponto de comunicação em uma rede. Quando aparece repetidamente em registros de tentativas de acesso, envio de mensagens indesejadas ou varreduras, uma base de reputação oferece contexto adicional.

O serviço reúne relatos enviados por sua comunidade e apresenta informações como quantidade, período, categorias e uma pontuação de confiança de abuso. Esses elementos enriquecem a investigação quando comparados aos registros do próprio sistema. Eles não substituem a evidência local.

Reputação não é prova absoluta. Um endereço pode ser compartilhado por muitas pessoas, pertencer a um provedor legítimo ou ter mudado de usuário. Também é possível que uma origem maliciosa ainda não tenha sido denunciada. Por isso, nem uma pontuação alta justifica sozinha uma resposta permanente, nem a ausência de relatos libera automaticamente uma conexão suspeita.

O próprio AbuseIPDB determina que um novo relato não seja criado apenas com base na pontuação existente. Isso produziria um ciclo em que a classificação alimenta denúncias sem observação independente. Um relato responsável precisa partir de atividade efetivamente registrada e seguir a política da plataforma.

Uma equipe pode consultar o IP de origem de várias tentativas malsucedidas de autenticação e comparar a reputação com horário, frequência, conta visada, resposta do servidor e outros eventos. Um bloqueio temporário ou uma limitação de tentativas pode decorrer do comportamento observado; a reputação atua como mais um elemento.

Ao relatar abuso, não copie registros completos sem revisão. Comentários podem revelar e-mails, nomes de usuários, caminhos internos, identificadores ou outros dados pessoais. A documentação orienta remover informações pessoais, e a chave da API deve ser protegida como uma senha.

## 5. Shodan: o que seus ativos mostram para a internet

O Shodan ajuda a responder: “Quais serviços e ativos meus estão publicamente visíveis na internet?”. Diferentemente de uma busca voltada a páginas, o Shodan indexa informações apresentadas por dispositivos e serviços conectados. Isso pode incluir tipo de software, opções suportadas, mensagens de identificação e outros metadados fornecidos durante a comunicação.

Para uma empresa, essa visão externa ajuda a descobrir como servidores, equipamentos e serviços próprios aparecem. Um serviço esquecido, uma porta que deveria estar restrita ou um software que divulga sua versão merece revisão. A consulta deve ser comparada a um inventário conhecido, não usada como substituta dele.

Exposição não equivale automaticamente a vulnerabilidade. Um serviço pode estar acessível por necessidade e protegido por autenticação, restrições de rede, atualização e monitoramento. Da mesma forma, algo que não aparece na busca não deve ser considerado invisível ou seguro: os dados podem estar desatualizados, incompletos ou associados a outro endereço.

O uso responsável fica limitado aos ativos da própria organização ou a ambientes para os quais exista autorização explícita. O objetivo é comparar o que deveria estar exposto com o que foi observado. Localizar um sistema de terceiro não concede permissão para acessá-lo, testá-lo ou explorar uma possível falha.

Uma pequena empresa pode manter uma lista de domínios, endereços IP públicos, serviços autorizados e responsáveis. Depois, consulta esses ativos no Shodan e confronta o resultado com o inventário. Se aparecer um serviço desconhecido, investiga internamente sua finalidade e configuração, sem tentar explorá-lo para “confirmar” um risco.

O Shodan oferece um recorte externo útil, mas não substitui varredura interna autorizada, gestão de vulnerabilidades, registros confiáveis nem monitoramento contínuo. Mudanças encontradas precisam voltar ao processo de inventário para que o conhecimento não se perca depois da consulta.

## 6. urlscan.io: como uma URL é carregada

O urlscan.io ajuda a responder: “Como determinada página ou URL se comporta quando acessada?”. O serviço abre a página em um ambiente de análise e registra elementos como redirecionamentos, domínios contatados, requisições, endereços IP, recursos carregados e uma imagem da página. Isso ajuda a investigar um link sem depender apenas de sua aparência.

Uma página pode redirecionar para outro domínio ou carregar recursos de várias origens. Esses dados oferecem pistas, mas não provam sozinhos que o endereço seja malicioso ou legítimo. Sites normais utilizam serviços externos, enquanto páginas maliciosas podem mudar de comportamento conforme localização, horário ou dispositivo.

O cuidado principal está na própria URL. Endereços podem conter identificadores de sessão, tokens de redefinição de senha, códigos de acesso, e-mails, números de pedido ou outros dados pessoais. Ao enviar o endereço completo, a pessoa pode tornar essas informações visíveis além do ambiente original.

O urlscan.io possui níveis de visibilidade pública, não listada e privada. A documentação informa que análises públicas aparecem na página inicial e nos resultados de busca. As não listadas não aparecem na busca pública, mas podem ser acessadas por pesquisadores e empresas avaliados no produto profissional. As privadas têm acesso mais restrito. Disponibilidade, retenção e condições atuais precisam ser verificadas antes do uso.

Imagine um e-mail com um link que imita o endereço de um fornecedor. Antes de enviar a URL, verifique se ela contém dados pessoais ou códigos de acesso. Se contiver, analise somente o domínio quando isso for suficiente, use um processo interno ou encaminhe o caso à equipe responsável. Se a URL for pública e não trouxer informações sensíveis, o relatório pode ajudar a observar redirecionamentos e recursos carregados.

## O que essas ferramentas não fazem

As seis ferramentas reduzem algumas incertezas, mas nenhuma entrega uma conclusão completa sobre a segurança de uma organização. Um resultado limpo não garante proteção. O Have I Been Pwned pode não conhecer determinado vazamento; o VirusTotal pode não detectar uma ameaça nova; uma base de reputação pode não ter relatos recentes; e um mecanismo de busca pode ainda não ter indexado uma mudança.

Uma detecção também não determina sozinha que existe um incidente. O alerta pode ser um falso positivo, uma configuração intencional ou um comportamento legítimo fora do padrão. A resposta deve considerar evidências do ambiente, impacto potencial e histórico. Quando o risco for relevante, preserve registros e envolva alguém qualificado antes de apagar arquivos ou alterar o sistema de forma precipitada.

Pontuações não substituem análise de risco. Uma nota baixa no HTTP Observatory aponta configurações que merecem atenção, mas não calcula todo o risco do negócio. Uma pontuação elevada no AbuseIPDB expressa dados derivados de relatos; ela não identifica, por si só, quem realizou uma atividade específica.

Exposição também não significa automaticamente vulnerabilidade. Um serviço visível pode ser necessário e estar protegido. A pergunta é se deveria estar exposto, se está atualizado, quem pode acessá-lo, quais dados processa e como a equipe detectaria um uso indevido.

## Cuidado com os dados enviados às ferramentas

A própria investigação de segurança não deve criar uma nova exposição de dados. Antes de usar um serviço externo, diferencie informação pública de informação confidencial. Um domínio institucional publicado já é visível na internet. Um endereço interno, contrato, relatório de cliente, token temporário ou arquivo com dados pessoais possui outro nível de risco.

URLs merecem atenção especial. Tudo o que aparece depois de um ponto de interrogação pode conter parâmetros usados pela aplicação. Eles às vezes incluem identificadores, e-mails, códigos de recuperação e tokens que concedem acesso. Copiar a URL inteira para uma plataforma pública pode expor muito mais do que o domínio investigado.

Arquivos também podem conter informações que não são imediatamente visíveis. Documentos de escritório guardam propriedades, comentários e histórico de edição. Imagens podem incluir metadados. Arquivos compactados podem reunir conteúdos que não foram revisados individualmente.

Antes do envio, faça uma pergunta simples: “Eu tenho autorização para enviar esta informação a esse serviço?”. Se a resposta for incerta, pare. Remova dados desnecessários, procure uma consulta por hash ou domínio, use uma solução interna aprovada ou peça orientação a quem responde por segurança e privacidade.

Não envie, sem avaliação e autorização adequadas, credenciais, senhas, chaves, tokens, contratos, bases de dados, documentos de clientes, arquivos internos, dados pessoais desnecessários ou links que concedam acesso. Também consulte a documentação e as condições atuais de cada serviço, pois recursos, limites, níveis de visibilidade, retenção e políticas podem mudar.

## Por onde começar?

[[visual:pergunta-e-ferramenta]]

Uma equipe pequena não precisa integrar todos os serviços de uma vez. Escolha uma pergunta real, documente de onde veio o sinal e faça uma consulta de baixo risco. Registre o resultado, suas limitações, a evidência disponível no ambiente e quem tomará a decisão.

Se a empresa ainda não possui inventário básico, comece listando sites, domínios, servidores, sistemas importantes, fornecedores, contas administrativas e responsáveis. Sem saber o que precisa ser protegido, até uma boa ferramenta produz resultados difíceis de priorizar.

Depois, escolha uma rotina pequena. Contas expostas podem entrar em uma revisão periódica de acesso. Configurações HTTP podem ser verificadas depois de mudanças importantes no site. Serviços externos observados devem ser comparados ao inventário. Eventos repetidos nos registros podem receber contexto de reputação, sem transformar essa reputação em bloqueio automático.

Defina também como registrar e encaminhar achados. Uma captura isolada no computador de uma pessoa desaparece quando ela fecha a janela. Um registro curto com data, ativo, pergunta, ferramenta, resultado, limitação e decisão cria continuidade para a equipe e permite revisar escolhas depois.

## Segurança não começa pela ferramenta

Uma ferramenta consegue mostrar sinais. Uma pessoa ou equipe precisa interpretar esses sinais dentro do contexto. As pessoas reconhecem comportamentos incomuns, seguem procedimentos e decidem quando pedir ajuda. A tecnologia oferece controles, registros e capacidade de análise. A transformação acontece quando esses elementos formam um processo repetível.

Segurança digital para pequenas empresas inclui atualização de sistemas, autenticação multifator, acesso limitado ao necessário, cópias de segurança testadas, monitoramento, orientação das equipes e um plano de resposta. As ferramentas gratuitas de cibersegurança complementam esse trabalho, mas não o substituem.

Se sua empresa precisa organizar segurança, infraestrutura ou processos tecnológicos, o primeiro passo não é instalar mais ferramentas. É entender quais ativos existem, quais riscos importam e quais controles precisam ser priorizados. A Koddahub pode ajudar a transformar esse diagnóstico em ações compatíveis com a realidade da operação.

## Perguntas frequentes

### Ferramentas gratuitas de cibersegurança são confiáveis?

Elas podem fornecer informações úteis quando usadas para a finalidade correta e interpretadas dentro do contexto. Nenhuma base é completa e nenhum scanner comprova que o ambiente inteiro esteja seguro. Também é necessário conferir a documentação e as condições atuais antes de enviar dados.

### O VirusTotal garante que um arquivo é seguro?

Não. A ausência de detecções significa apenas que os mecanismos consultados não identificaram sinais conhecidos naquele momento. Ameaças novas ou dependentes de condições específicas podem não ser reconhecidas. Uma detecção isolada também pode ser um falso positivo.

### Posso verificar qualquer domínio ou endereço IP?

Consultas passivas sobre informações públicas podem ser possíveis, mas isso não autoriza testar, acessar ou explorar sistemas de terceiros. Para avaliações ativas, use somente ativos próprios ou ambientes para os quais exista autorização explícita.

### Shodan é uma ferramenta de invasão?

Não. O Shodan é um mecanismo de busca de dispositivos e serviços conectados à internet. Pode ser usado defensivamente para observar como ativos próprios aparecem externamente. Localizar um serviço não concede autorização para acessá-lo ou explorá-lo.

### Uma nota alta no HTTP Observatory significa que meu site está seguro?

Não. A nota avalia um conjunto de configurações HTTP e boas práticas relacionadas. Ela não verifica todas as vulnerabilidades possíveis, como falhas na aplicação, componentes desatualizados, problemas de autenticação ou armazenamento inadequado de senhas.

### Posso enviar documentos de clientes para ferramentas de análise?

Não sem avaliação específica, autorização apropriada e confirmação de que o serviço e o contrato são adequados para esses dados. Em ferramentas públicas, não envie documentos de clientes, contratos, credenciais, tokens ou arquivos confidenciais.

## Links internos sugeridos

- /blog/e-seguro-usar-claude/

## Referências para revisão

Have I Been Pwned, perguntas frequentes e limites das consultas: https://haveibeenpwned.com/FAQs

VirusTotal, funcionamento das análises e compartilhamento de resultados: https://docs.virustotal.com/docs/how-it-works

MDN HTTP Observatory, perguntas frequentes e limites da pontuação: https://developer.mozilla.org/en-US/observatory/docs/faq

MDN HTTP Observatory, testes e método de pontuação: https://developer.mozilla.org/en-US/observatory/docs/tests_and_scoring

AbuseIPDB, documentação da API e cuidados com dados pessoais: https://docs.abuseipdb.com/

AbuseIPDB, política para relatos de atividades abusivas: https://www.abuseipdb.com/reporting-policy

Shodan Help Center, definição e informações indexadas: https://help.shodan.io/the-basics/what-is-shodan

Shodan Help Center, monitoramento de redes e ativos conhecidos: https://help.shodan.io/shodan-monitor/network-vs-domain-vs-query

urlscan.io, níveis de visibilidade das análises: https://docs.urlscan.io/pages/visibility

urlscan.io, perguntas frequentes sobre privacidade e visibilidade: https://urlscan.io/docs/faq/

CISA Cyber Essentials, controles básicos de preparação: https://www.cisa.gov/sites/default/files/publications/19_1106_cisa_CISA_Cyber_Essentials_S508C_0.pdf
