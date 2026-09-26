# Database do Portal KoddaHub

## Objetivo e ambiente

Este diretório versiona o schema inicial do Portal de Suporte multi-organização. O alvo é PostgreSQL 16, database `koddahub_support` e role de aplicação `koddahub_support_app`. As migrations não criam database, role, credenciais ou dados fictícios.

Nenhuma migration foi aplicada durante a criação deste schema. O host de desenvolvimento não possuía `psql`; a validação realizada foi exclusivamente estática.

## Ordem das migrations

1. `001_create_organizations.sql` — organizações/clientes.
2. `002_create_users.sql` — identidade lógica das pessoas.
3. `003_create_user_identities.sql` — vínculos com provedores externos.
4. `004_create_organization_members.sql` — associação e papel na organização.
5. `005_create_products.sql` — catálogo de produtos/serviços.
6. `006_create_organization_products.sql` — produtos disponíveis por organização.
7. `007_create_tickets.sql` — chamados de suporte.
8. `008_create_ticket_messages.sql` — conversa do chamado.
9. `009_create_ticket_attachments.sql` — metadados de anexos.
10. `010_create_ticket_events.sql` — eventos auditáveis da timeline.
11. `011_create_support_indexes.sql` — índices de acesso previsível.

As migrations devem ser aplicadas uma vez, na ordem numérica e por uma ferramenta que interrompa o processo ao primeiro erro. Antes de uso futuro, configure a conexão fora do repositório, confirme explicitamente database e role e execute inicialmente em ambiente não produtivo. Nunca coloque senhas, tokens, connection strings com credencial ou outros secrets no Git, em comandos registrados ou em `ticket_events.metadata`.

## Modelo e responsabilidades

O diagrama e os relacionamentos estão em [schema.md](schema.md).

- `organizations`: raiz de isolamento dos clientes.
- `users`: pessoa lógica, independente da autenticação e da organização.
- `user_identities`: identificador externo de autenticação; não armazena tokens.
- `organization_members`: vínculo de autorização com papéis mínimos `owner`, `admin` e `member`.
- `products`: catálogo global atendido pela KoddaHub.
- `organization_products`: disponibilidade de produto por organização.
- `tickets`: cabeçalho do chamado, produto, prioridade, estado e responsáveis.
- `ticket_messages`: conteúdo textual, incluindo a descrição inicial como primeira mensagem.
- `ticket_attachments`: referência de storage associada a uma mensagem; nunca o binário.
- `ticket_events`: mudanças estruturadas relevantes, com JSONB apenas para contexto complementar.

O login existente menciona Google, LinkedIn e senha local, mas ainda é apenas uma interface sem autenticação implementada. Por isso, o schema não assume provedor obrigatório, não cria coluna de senha e deixa `provider` extensível. Caso autenticação local seja aprovada futuramente, seu segredo deverá usar mecanismo próprio e hash adequado, nunca texto simples.

Os e-mails são gravados já canonicalizados com `lower(btrim(email))` e têm unicidade global. A aplicação deve canonicalizar antes do `INSERT`/`UPDATE`; a constraint recusa valores fora desse formato sem tentar implementar validação RFC completa.

## Integridade e ciclo de vida

Um ticket referencia `(organization_id, product_id)` pela chave única de `organization_products`. Assim, uma organização não pode abrir chamado para produto arbitrário. O criador e o responsável são usuários globais: autorização para cada operação continua sendo responsabilidade do backend futuro.

As FKs usam `ON DELETE RESTRICT`. O schema preserva histórico operacional e exige desativação por `status` em vez de apagar organizações, pessoas, produtos ou relações já referenciadas. Não há cascatas destrutivas.

`updated_at` usa `DEFAULT CURRENT_TIMESTAMP`, mas não é atualizado automaticamente. A aplicação futura deve definir `updated_at = CURRENT_TIMESTAMP` em todo update. Essa opção evita triggers enquanto não existe backend e mantém as migrations simples; pode ser substituída por uma função/trigger compartilhada em migration posterior, se houver necessidade comprovada.

O corpo inicial informado na abertura do chamado é a primeira `ticket_message`, evitando duplicação em `tickets`. Mensagens não possuem `updated_at`, pois edição ainda não foi confirmada. Anexos pertencem a mensagens e guardam apenas nome original, chave opaca de storage, tipo, tamanho e autor. `storage_key` não pode ser caminho absoluto nem URL assinada por contrato da aplicação.

Eventos aceitam somente tipos previstos. `metadata` deve ser objeto JSON e serve para valores anteriores/novos ou contexto equivalente; chaves relacionais principais permanecem em colunas e tabelas próprias. O ator pode ser nulo para um evento futuro produzido pelo sistema.

## Validação e execução futura

A validação local disponível é estática:

```bash
python3 -m unittest tests.test_database_migrations -v
git diff --check -- database/ tests/test_database_migrations.py
```

Ela verifica sequência, transações, tabelas, FKs essenciais, constraints, índices e padrões perigosos, mas não comprova sintaxe nem execução no PostgreSQL. Antes da primeira aplicação real, resta validar todas as migrations em uma instância descartável de PostgreSQL 16 e ensaiar rollback operacional.

Uma execução futura, depois de revisão e autorização, pode usar uma ferramenta de migrations ou `psql` configurado por variáveis/arquivo seguro. Não copie uma senha para o comando, README ou log. Registre versão aplicada, checksum, horário e resultado sem credenciais.
