#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" != "--confirm-hml-clean" ]; then
    printf '%s\n' 'Uso: clean-hml.sh --confirm-hml-clean' >&2
    exit 1
fi

environment="$(docker inspect koddahub-support-api --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -n 's/^SUPPORT_ENVIRONMENT=//p')"
if [ "$environment" = "production" ]; then
    printf '%s\n' 'ERRO: limpeza HML bloqueada em production.' >&2
    exit 1
fi

docker exec -i koddahub-support-db psql -U postgres -d koddahub_support --set=ON_ERROR_STOP=1 <<'SQL'
BEGIN;
DELETE FROM ticket_attachments WHERE message_id IN (
    SELECT m.id FROM ticket_messages m JOIN tickets t ON t.id=m.ticket_id
    JOIN organizations o ON o.id=t.organization_id WHERE o.slug='koddahub-hml'
);
DELETE FROM ticket_events WHERE ticket_id IN (SELECT t.id FROM tickets t JOIN organizations o ON o.id=t.organization_id WHERE o.slug='koddahub-hml');
DELETE FROM ticket_messages WHERE ticket_id IN (SELECT t.id FROM tickets t JOIN organizations o ON o.id=t.organization_id WHERE o.slug='koddahub-hml');
DELETE FROM tickets WHERE organization_id=(SELECT id FROM organizations WHERE slug='koddahub-hml');
COMMIT;
SQL
printf '%s\n' 'Tickets e histórico HML removidos; identidade e catálogo foram preservados.'
