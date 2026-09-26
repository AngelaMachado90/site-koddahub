-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 011_create_support_indexes.sql
-- Objetivo    : Criar índices para as consultas previsíveis do Portal.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE INDEX organization_members_user_idx
    ON organization_members (user_id, status);

CREATE INDEX organization_products_product_idx
    ON organization_products (product_id, status);

CREATE INDEX tickets_organization_updated_idx
    ON tickets (organization_id, updated_at DESC);

CREATE INDEX tickets_organization_status_updated_idx
    ON tickets (organization_id, status, updated_at DESC);

CREATE INDEX tickets_assigned_status_updated_idx
    ON tickets (assigned_to_user_id, status, updated_at DESC)
    WHERE assigned_to_user_id IS NOT NULL;

CREATE INDEX tickets_product_updated_idx
    ON tickets (product_id, updated_at DESC);

CREATE INDEX ticket_messages_ticket_created_idx
    ON ticket_messages (ticket_id, created_at, id);

CREATE INDEX ticket_attachments_message_idx
    ON ticket_attachments (message_id, created_at);

CREATE INDEX ticket_events_ticket_created_idx
    ON ticket_events (ticket_id, created_at, id);

COMMIT;
