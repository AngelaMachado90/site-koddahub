-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 005_create_products.sql
-- Objetivo    : Cadastrar produtos ou serviços atendidos pelo Portal.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    slug VARCHAR(160) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT products_name_not_blank CHECK (btrim(name) <> ''),
    CONSTRAINT products_slug_not_blank CHECK (btrim(slug) <> ''),
    CONSTRAINT products_slug_format
        CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    CONSTRAINT products_status_valid
        CHECK (status IN ('active', 'inactive')),
    CONSTRAINT products_slug_unique UNIQUE (slug)
);

COMMIT;
