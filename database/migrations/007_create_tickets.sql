-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 007_create_tickets.sql
-- Objetivo    : Criar a entidade central de chamados de suporte.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE tickets (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reference_code VARCHAR(40) NOT NULL,
    organization_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    created_by_user_id BIGINT NOT NULL,
    assigned_to_user_id BIGINT,
    title VARCHAR(160) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'open',
    priority VARCHAR(10) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMPTZ,

    CONSTRAINT tickets_reference_code_not_blank
        CHECK (btrim(reference_code) <> ''),
    CONSTRAINT tickets_reference_code_format
        CHECK (reference_code ~ '^[A-Z0-9]+(?:-[A-Z0-9]+)*$'),
    CONSTRAINT tickets_reference_code_unique UNIQUE (reference_code),
    CONSTRAINT tickets_title_not_blank CHECK (btrim(title) <> ''),
    CONSTRAINT tickets_status_valid CHECK (status IN (
        'open', 'in_progress', 'waiting_customer', 'resolved', 'closed'
    )),
    CONSTRAINT tickets_priority_valid
        CHECK (priority IN ('p1', 'p2', 'p3', 'p4')),
    CONSTRAINT tickets_closed_at_consistent CHECK (
        (status = 'closed' AND closed_at IS NOT NULL)
        OR (status <> 'closed' AND closed_at IS NULL)
    ),
    CONSTRAINT tickets_organization_product_fk
        FOREIGN KEY (organization_id, product_id)
        REFERENCES organization_products (organization_id, product_id)
        ON DELETE RESTRICT,
    CONSTRAINT tickets_created_by_user_fk FOREIGN KEY (created_by_user_id)
        REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT tickets_assigned_to_user_fk FOREIGN KEY (assigned_to_user_id)
        REFERENCES users (id) ON DELETE RESTRICT
);

COMMIT;
