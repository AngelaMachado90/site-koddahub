# Infraestrutura local/HML do Portal de Suporte

Esta stack cria um PostgreSQL 16 dedicado ao Portal, isolado do PostgreSQL do n8n. Ela não publica a porta 5432 no host e utiliza rede interna e volume persistente próprios.

## Recursos

- container: `koddahub-support-db`;
- network interna: `koddahub-support-db`;
- volume: `koddahub-support-postgres-data`;
- database: `koddahub_support`;
- role de aplicação: `koddahub_support_app`.

Os secrets ficam exclusivamente em `/srv/koddahub/support/secrets`, fora do repositório, com acesso restrito. O Compose os monta como arquivos somente leitura em `/run/secrets`; os scripts leem o conteúdo internamente e nunca o recebem como argumento de processo. Nunca copie seus valores para comandos, logs, documentação ou Git.

## Privilégios iniciais

O bootstrap cria o database e concede à role da aplicação somente `CONNECT` no database e `USAGE` no schema `public`. A role não é superuser, não cria databases ou roles e não cria tabelas. Após a aplicação controlada das migrations, devem ser concedidos apenas os privilégios DML e de sequences necessários ao backend.

As migrations são responsabilidade do checkpoint específico e não são executadas automaticamente ao subir o PostgreSQL. A role de runtime não possui DDL; migrations futuras devem usar o contexto administrativo/migrator controlado e depois conceder somente DML e uso de sequences à aplicação.

## Bootstrap

Em volume vazio, `initdb/001-create-support-database.sh` é chamado automaticamente pelo entrypoint e delega para o procedimento idempotente `scripts/bootstrap-existing.sh`.

Em um cluster já inicializado, o mesmo procedimento pode ser executado conscientemente dentro do container, sem apagar o volume:

```bash
docker exec --user 0 koddahub-support-db /opt/koddahub-support/scripts/bootstrap-existing.sh
```

O procedimento aguarda o PostgreSQL por um período limitado, cria role e database somente quando ausentes, reaplica atributos restritivos e permissões mínimas e não executa migrations.

## Migrations

`scripts/migrate.sh` aplica os arquivos de `database/migrations` em ordem lexical. O runner usa `ON_ERROR_STOP`, registra nome, SHA-256 e horário em `schema_migrations` e bloqueia uma migration conhecida cujo arquivo tenha checksum diferente. A gravação do controle substitui o `COMMIT` final do fluxo enviado ao PostgreSQL, ficando na mesma transação da migration sem alterar o arquivo versionado.

```bash
infra/support/scripts/migrate.sh
```

O runner utiliza o contexto administrativo local do container. Ao final, concede à role runtime DML nas tabelas de domínio e uso das sequences, revogando explicitamente qualquer acesso a `schema_migrations`.

## Operação

Execute o Compose a partir deste diretório. Antes de qualquer mudança, confira os recursos existentes e o estado da stack. Não remova o volume em operações rotineiras: ele contém os dados persistentes.

### API local/HML

A API FastAPI é construída pelo serviço `api` e publicada somente em `127.0.0.1:8011`. Ela participa da rede interna do database e de uma bridge própria para o binding local; o PostgreSQL participa apenas da rede interna e continua sem porta no host.

```bash
docker compose -f infra/support/compose.yaml build api
docker compose -f infra/support/compose.yaml up -d
curl http://127.0.0.1:8011/health
docker compose -f infra/support/compose.yaml stop api
```

Testes do backend usam fixtures temporárias e exigem habilitação explícita:

```bash
docker compose -f infra/support/compose.yaml run --rm \
  -e SUPPORT_TEST_DATABASE=true api \
  python -m unittest discover -s tests -v
```

Em development/HML, organização e usuário vêm exclusivamente das variáveis controladas da stack, nunca do browser. Essa identidade é bloqueada quando `SUPPORT_ENVIRONMENT=production`; ela não representa autenticação real. OAuth, autorização produtiva, observabilidade e proteção pública continuam pendentes.

O seed mínimo não roda no startup. Em LOCAL/HML, execute-o conscientemente e recrie a API para carregar os IDs resolvidos do banco:

```bash
infra/support/scripts/seed-hml.sh --confirm-hml
docker compose -f infra/support/compose.yaml up -d api
```

O script é idempotente, cria apenas organização, usuário, membership e dois produtos HML, e grava os IDs técnicos em `/srv/koddahub/support/runtime/hml.env`. Ele não cria tickets e se recusa a operar quando a stack estiver configurada como production.

Para remover conscientemente apenas tickets e histórico da organização HML, preservando identidade e catálogo:

```bash
infra/support/scripts/clean-hml.sh --confirm-hml-clean
```

As versões Python ficam fixadas em `backend/requirements.txt`. Atualizações devem ser deliberadas, seguidas de rebuild e execução integral dos testes.

O healthcheck consulta o catálogo administrativo para confirmar a existência de `koddahub_support` e executa `SELECT 1` nesse database. Assim, um servidor PostgreSQL vazio não é considerado funcional para o Portal.

Backups locais ficam fora do Git em `/srv/koddahub/support/backups`, montado como `/backups` no container. O baseline de schema é produzido com `pg_dump --schema-only`, sem credenciais na linha de comando. O procedimento completo de retenção e restore será consolidado antes de declarar o serviço pronto para produção. Até lá, esta infraestrutura deve ser tratada somente como LOCAL/HML.
