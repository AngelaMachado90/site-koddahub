#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" != "--confirm-hml" ]; then
    printf '%s\n' 'Uso: seed-hml.sh --confirm-hml' >&2
    exit 1
fi

environment="$(docker inspect koddahub-support-api --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -n 's/^SUPPORT_ENVIRONMENT=//p')"
if [ "$environment" = "production" ]; then
    printf '%s\n' 'ERRO: seed HML bloqueado em production.' >&2
    exit 1
fi

seed_output="$(docker exec -i koddahub-support-db psql -U postgres -d koddahub_support -At --set=ON_ERROR_STOP=1 <<'SQL'
BEGIN;
INSERT INTO organizations (name, slug, status)
VALUES ('KoddaHub HML', 'koddahub-hml', 'active')
ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name, status = 'active', updated_at = CURRENT_TIMESTAMP;

INSERT INTO users (name, email, status)
VALUES ('Usuário HML', 'usuario.hml@example.invalid', 'active')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, status = 'active', updated_at = CURRENT_TIMESTAMP;

INSERT INTO products (name, slug, status) VALUES
    ('Kiwi TCMS', 'kiwi-tcms', 'active'),
    ('Portal de Suporte', 'portal-de-suporte', 'active')
ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name, status = 'active', updated_at = CURRENT_TIMESTAMP;

INSERT INTO organization_members (organization_id, user_id, role, status)
SELECT o.id, u.id, 'owner', 'active'
FROM organizations o CROSS JOIN users u
WHERE o.slug = 'koddahub-hml' AND u.email = 'usuario.hml@example.invalid'
ON CONFLICT (organization_id, user_id)
DO UPDATE SET role = 'owner', status = 'active', updated_at = CURRENT_TIMESTAMP;

INSERT INTO organization_products (organization_id, product_id, status)
SELECT o.id, p.id, 'active'
FROM organizations o CROSS JOIN products p
WHERE o.slug = 'koddahub-hml' AND p.slug IN ('kiwi-tcms', 'portal-de-suporte')
ON CONFLICT (organization_id, product_id)
DO UPDATE SET status = 'active', updated_at = CURRENT_TIMESTAMP;

SELECT o.id || '|' || u.id
FROM organizations o CROSS JOIN users u
WHERE o.slug = 'koddahub-hml' AND u.email = 'usuario.hml@example.invalid';
COMMIT;
SQL
)"
ids="$(printf '%s\n' "$seed_output" | grep -E '^[0-9]+\|[0-9]+$' | tail -n 1)"

if [[ ! "$ids" =~ ^[0-9]+\|[0-9]+$ ]]; then
    printf '%s\n' 'ERRO: IDs HML não puderam ser resolvidos.' >&2
    exit 1
fi

organization_id="${ids%%|*}"
user_id="${ids##*|}"
runtime_dir="/srv/koddahub/support/runtime"
runtime_file="$runtime_dir/hml.env"
install -d -m 0700 "$runtime_dir"
temporary="$(mktemp "$runtime_dir/hml.env.XXXXXX")"
printf 'SUPPORT_DEV_ORGANIZATION_ID=%s\nSUPPORT_DEV_USER_ID=%s\n' \
    "$organization_id" "$user_id" >"$temporary"
chmod 0600 "$temporary"
mv "$temporary" "$runtime_file"
printf 'HML seed pronto: organization_id=%s user_id=%s\n' "$organization_id" "$user_id"
