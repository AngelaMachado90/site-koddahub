-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 009_create_ticket_attachments.sql
-- Objetivo    : Registrar metadados de anexos associados a mensagens.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE ticket_attachments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    message_id BIGINT NOT NULL,
    uploaded_by_user_id BIGINT NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    storage_key TEXT NOT NULL,
    content_type VARCHAR(255),
    size_bytes BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ticket_attachments_filename_not_blank
        CHECK (btrim(original_filename) <> ''),
    CONSTRAINT ticket_attachments_storage_key_not_blank
        CHECK (btrim(storage_key) <> ''),
    CONSTRAINT ticket_attachments_content_type_not_blank
        CHECK (content_type IS NULL OR btrim(content_type) <> ''),
    CONSTRAINT ticket_attachments_size_nonnegative CHECK (size_bytes >= 0),
    CONSTRAINT ticket_attachments_storage_key_unique UNIQUE (storage_key),
    CONSTRAINT ticket_attachments_message_fk FOREIGN KEY (message_id)
        REFERENCES ticket_messages (id) ON DELETE RESTRICT,
    CONSTRAINT ticket_attachments_uploaded_by_user_fk
        FOREIGN KEY (uploaded_by_user_id) REFERENCES users (id)
        ON DELETE RESTRICT
);

COMMIT;
