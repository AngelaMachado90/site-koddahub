#!/bin/sh
set -eu

app_secret_file="/run/secrets/postgres_app_password"

if [ ! -r "$app_secret_file" ]; then
    printf '%s\n' 'ERRO: secret da aplicação não está legível.' >&2
    exit 1
fi

postgres_ready=false
attempt=1
while [ "$attempt" -le 30 ]; do
    if pg_isready --username postgres --dbname postgres >/dev/null 2>&1; then
        postgres_ready=true
        break
    fi
    sleep 1
    attempt=$((attempt + 1))
done

if [ "$postgres_ready" != "true" ]; then
    printf '%s\n' 'ERRO: PostgreSQL não ficou disponível para o bootstrap.' >&2
    exit 1
fi

app_password="$(cat "$app_secret_file")"
role_exists="$(
    psql --username postgres --dbname postgres --tuples-only --no-align \
        --set=ON_ERROR_STOP=1 \
        --command "SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'koddahub_support_app');"
)"

if [ "$role_exists" = "f" ]; then
    psql --username postgres --dbname postgres --set=ON_ERROR_STOP=1 \
        --set=app_password="$app_password" <<'SQL'
CREATE ROLE koddahub_support_app
    LOGIN
    PASSWORD :'app_password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOREPLICATION;
SQL
else
    psql --username postgres --dbname postgres --set=ON_ERROR_STOP=1 \
        --set=app_password="$app_password" <<'SQL'
ALTER ROLE koddahub_support_app
    LOGIN
    PASSWORD :'app_password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOREPLICATION;
SQL
fi

database_exists="$(
    psql --username postgres --dbname postgres --tuples-only --no-align \
        --set=ON_ERROR_STOP=1 \
        --command "SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'koddahub_support');"
)"

if [ "$database_exists" = "f" ]; then
    createdb --username postgres --owner postgres koddahub_support
fi

psql --username postgres --dbname postgres --set=ON_ERROR_STOP=1 <<'SQL'
REVOKE ALL ON DATABASE koddahub_support FROM PUBLIC;
GRANT CONNECT ON DATABASE koddahub_support TO koddahub_support_app;
SQL

psql --username postgres --dbname koddahub_support \
    --set=ON_ERROR_STOP=1 <<'SQL'
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM koddahub_support_app;
GRANT USAGE ON SCHEMA public TO koddahub_support_app;
SQL

unset app_password
printf '%s\n' 'Bootstrap do database de suporte concluído.'
