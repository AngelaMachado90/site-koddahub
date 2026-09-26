-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 002_create_users.sql
-- Objetivo    : Criar as pessoas usuárias lógicas do Portal KoddaHub.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    email VARCHAR(320) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT users_name_not_blank CHECK (btrim(name) <> ''),
    CONSTRAINT users_email_canonical
        CHECK (email = lower(btrim(email)) AND position('@' IN email) > 1),
    CONSTRAINT users_status_valid
        CHECK (status IN ('active', 'inactive', 'suspended')),
    CONSTRAINT users_email_unique UNIQUE (email)
);

COMMIT;
