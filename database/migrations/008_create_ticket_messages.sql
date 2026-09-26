-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 008_create_ticket_messages.sql
-- Objetivo    : Registrar a conversa textual dos chamados.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE ticket_messages (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    author_user_id BIGINT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ticket_messages_body_not_blank CHECK (btrim(body) <> ''),
    CONSTRAINT ticket_messages_ticket_fk FOREIGN KEY (ticket_id)
        REFERENCES tickets (id) ON DELETE RESTRICT,
    CONSTRAINT ticket_messages_author_user_fk FOREIGN KEY (author_user_id)
        REFERENCES users (id) ON DELETE RESTRICT
);

COMMIT;
