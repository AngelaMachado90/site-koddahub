---
title: "Critérios de aceite evitam interpretações"
seo_title: 'Critérios de aceite: como tornar uma demanda verificável'
meta_description: Critérios de aceite traduzem uma necessidade em comportamentos que podem ser observados.
slug: "criterios-de-aceite"
category: "Desenvolvimento"
reading_time: 2 minutos
summary: Critérios de aceite traduzem uma necessidade em comportamentos que podem ser observados.
planned_date: 29/09/2026
publish_date: 2026-09-29
status: "review"
author: VAL — Valor, Autoridade e Linguagem Koddahub
tags: [Desenvolvimento, Processos]
reviewed_at: 2026-09-15
review_blockers: [conteúdo abaixo de 15 minutos, capa definitiva ausente, glossário pendente, recurso visual pendente, QA mobile final pendente]
---
# Critérios de aceite evitam interpretações

Critérios de aceite traduzem uma necessidade em comportamentos que podem ser observados. Eles não substituem conversa, mas reduzem a chance de cada pessoa imaginar um resultado diferente.

## Comece por uma situação concreta

“Cadastro deve funcionar” é amplo demais. Especifique o que acontece quando os dados são válidos, quando falta um campo e quando o registro já existe. A mensagem é compreensível? O usuário pode corrigir? O sistema mantém os dados preenchidos? Esses detalhes afetam experiência, implementação e teste.

## Separe regra de interface

Uma regra pode dizer que determinado campo é obrigatório; a interface decide como explicar isso. Registre pré-condições, entrada, ação e resultado esperado sem impor um componente visual desnecessário. Marque dúvidas ainda não decididas em vez de escondê-las em frases vagas.

## Verifique com três olhares

Peça a alguém de negócio que confirme o objetivo, a quem implementa que avalie viabilidade e a QA que formule cenários de teste. Se ninguém consegue distinguir sucesso de falha a partir do texto, o critério precisa de refinamento. Depois da entrega, use os mesmos critérios para validar a versão real, incluindo exceções e mensagens.

Critério de aceite bom não descreve tudo que o sistema poderá fazer um dia. Ele delimita o comportamento desta entrega e torna as decisões rastreáveis.

## Referências para revisão

Exemplo hipotético; adaptar regras ao domínio e à legislação aplicável quando houver.
