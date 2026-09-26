#!/usr/bin/env bash
set -euo pipefail

script_path="$(readlink -f "${BASH_SOURCE[0]}")"
script_dir="${script_path%/*}"
project_root="$(readlink -f "$script_dir/../../..")"
migrations_dir="${MIGRATIONS_DIR:-$project_root/database/migrations}"
db_container="${DB_CONTAINER:-koddahub-support-db}"
lock_file="${MIGRATION_LOCK_FILE:-/tmp/koddahub-support-migrate.lock}"

exec 9>"$lock_file"
if ! flock -n 9; then
    printf '%s\n' 'ERRO: outro migration runner está em execução.' >&2
    exit 1
fi

if [ ! -d "$migrations_dir" ]; then
    printf 'ERRO: diretório de migrations não existe: %s\n' "$migrations_dir" >&2
    exit 1
fi

mapfile -t migrations < <(
    find "$migrations_dir" -maxdepth 1 -type f \
        -name '[0-9][0-9][0-9]_*.sql' -printf '%f\n' | sort
)

if [ "${#migrations[@]}" -eq 0 ]; then
    printf '%s\n' 'ERRO: nenhuma migration encontrada.' >&2
    exit 1
fi

docker exec -i "$db_container" psql \
    --username postgres --dbname koddahub_support \
    --set=ON_ERROR_STOP=1 <<'SQL'
CREATE TABLE IF NOT EXISTS schema_migrations (
    filename TEXT PRIMARY KEY,
    checksum_sha256 CHAR(64) NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT schema_migrations_filename_not_blank
        CHECK (btrim(filename) <> ''),
    CONSTRAINT schema_migrations_checksum_format
        CHECK (checksum_sha256 ~ '^[0-9a-f]{64}$')
);
REVOKE ALL ON TABLE schema_migrations FROM PUBLIC;
REVOKE ALL ON TABLE schema_migrations FROM koddahub_support_app;
SQL

applied=0
known=0

for filename in "${migrations[@]}"; do
    path="$migrations_dir/$filename"
    checksum="$(sha256sum "$path" | awk '{print $1}')"

    if [ "$(tail -n 1 "$path")" != 'COMMIT;' ]; then
        printf 'ERRO: %s não termina com COMMIT;.\n' "$filename" >&2
        exit 1
    fi

    stored_checksum="$(
        printf '%s\n' \
            "SELECT checksum_sha256 FROM schema_migrations WHERE filename = :'migration_filename';" |
            docker exec -i "$db_container" psql \
                --username postgres --dbname koddahub_support \
                --tuples-only --no-align --set=ON_ERROR_STOP=1 \
                --set=migration_filename="$filename"
    )"

    if [ -n "$stored_checksum" ]; then
        if [ "$stored_checksum" != "$checksum" ]; then
            printf 'ERRO: checksum divergente para %s.\n' "$filename" >&2
            exit 1
        fi
        printf 'JÁ APLICADA %s sha256=%s\n' "$filename" "$checksum"
        known=$((known + 1))
        continue
    fi

    printf 'APLICANDO %s sha256=%s\n' "$filename" "$checksum"
    {
        sed '$d' "$path"
        printf '%s\n' \
            "INSERT INTO schema_migrations (filename, checksum_sha256)" \
            "VALUES (:'migration_filename', :'migration_checksum');" \
            "COMMIT;"
    } | docker exec -i "$db_container" psql \
        --username postgres --dbname koddahub_support \
        --set=ON_ERROR_STOP=1 \
        --set=migration_filename="$filename" \
        --set=migration_checksum="$checksum"
    printf 'APLICADA %s sha256=%s\n' "$filename" "$checksum"
    applied=$((applied + 1))
done

docker exec -i "$db_container" psql \
    --username postgres --dbname koddahub_support \
    --set=ON_ERROR_STOP=1 <<'SQL'
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA public TO koddahub_support_app;
GRANT USAGE, SELECT
    ON ALL SEQUENCES IN SCHEMA public TO koddahub_support_app;
REVOKE ALL ON TABLE schema_migrations FROM koddahub_support_app;
SQL

printf 'RESUMO applied=%s known=%s total=%s\n' \
    "$applied" "$known" "${#migrations[@]}"
