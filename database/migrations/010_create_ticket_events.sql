-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 010_create_ticket_events.sql
-- Objetivo    : Registrar eventos estruturados da timeline dos chamados.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE ticket_events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    actor_user_id BIGINT,
    event_type VARCHAR(40) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ticket_events_type_valid CHECK (event_type IN (
        'created', 'status_changed', 'priority_changed',
        'assignee_changed', 'product_changed'
    )),
    CONSTRAINT ticket_events_metadata_object
        CHECK (jsonb_typeof(metadata) = 'object'),
    CONSTRAINT ticket_events_ticket_fk FOREIGN KEY (ticket_id)
        REFERENCES tickets (id) ON DELETE RESTRICT,
    CONSTRAINT ticket_events_actor_user_fk FOREIGN KEY (actor_user_id)
        REFERENCES users (id) ON DELETE RESTRICT
);

COMMIT;
