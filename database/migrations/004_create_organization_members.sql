-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 004_create_organization_members.sql
-- Objetivo    : Vincular usuários a organizações e definir autorização básica.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE organization_members (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT organization_members_role_valid
        CHECK (role IN ('owner', 'admin', 'member')),
    CONSTRAINT organization_members_status_valid
        CHECK (status IN ('active', 'inactive')),
    CONSTRAINT organization_members_organization_user_unique
        UNIQUE (organization_id, user_id),
    CONSTRAINT organization_members_organization_fk
        FOREIGN KEY (organization_id) REFERENCES organizations (id)
        ON DELETE RESTRICT,
    CONSTRAINT organization_members_user_fk FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT
);

COMMIT;
