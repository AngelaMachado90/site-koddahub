-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 003_create_user_identities.sql
-- Objetivo    : Desacoplar usuários dos provedores externos de autenticação.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE user_identities (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    provider VARCHAR(80) NOT NULL,
    provider_subject VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT user_identities_provider_not_blank
        CHECK (btrim(provider) <> ''),
    CONSTRAINT user_identities_provider_canonical
        CHECK (provider = lower(btrim(provider))
            AND provider ~ '^[a-z0-9][a-z0-9._-]*$'),
    CONSTRAINT user_identities_subject_not_blank
        CHECK (btrim(provider_subject) <> ''),
    CONSTRAINT user_identities_provider_subject_unique
        UNIQUE (provider, provider_subject),
    CONSTRAINT user_identities_user_provider_unique
        UNIQUE (user_id, provider),
    CONSTRAINT user_identities_user_fk FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT
);

COMMIT;
