# KoddaHub

Site institucional da KoddaHub.

## Desenvolvimento

```bash
python3 scripts/build.py
```

O código editável fica em `public/`. O resultado público é gerado em `dist/` e não deve ser editado manualmente.

## Design System

A identidade visual, os tokens e os componentes da marca estão documentados no
[Koddahub Design System](docs/design-system/README.md). Os tokens em
`public/assets/css/koddahub-tokens.css` são a fonte de verdade da interface.

## Chatbot

O launcher do chatbot fica no canto inferior direito e usa a identidade do
Design System. O botão circular mede 64 × 64 px no desktop e 56 × 56 px no
mobile. O texto “Tire suas dúvidas” aparece como tooltip em hover ou foco; o
nome acessível permanece disponível por `aria-label`.

A lógica de abertura e mensagens está em `public/assets/js/site.js`. O endpoint
é definido pela constante `CHAT_WEBHOOK_URL`. Enquanto ela permanecer com o
valor `COLOQUE_AQUI_O_WEBHOOK`, o launcher visual pode ser validado, mas o envio
de mensagens não deve ser considerado funcional nem publicado em produção.

## Publicação

Produção usa `/home/kodda/public_html`. Não há ambiente de staging, homologação
ou HML configurado atualmente. Produção não deve ser usada como staging; um
deploy produtivo requer build validado, staging aprovado ou autorização
excepcional explícita e plano de rollback.
