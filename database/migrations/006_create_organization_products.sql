-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- Migration   : 006_create_organization_products.sql
-- Objetivo    : Definir os produtos disponíveis para cada organização.
-- Database    : koddahub_support
-- Owner/Role  : koddahub_support_app
-- PostgreSQL  : 16
-- ============================================================================

BEGIN;

CREATE TABLE organization_products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT organization_products_status_valid
        CHECK (status IN ('active', 'inactive')),
    CONSTRAINT organization_products_organization_product_unique
        UNIQUE (organization_id, product_id),
    CONSTRAINT organization_products_organization_fk
        FOREIGN KEY (organization_id) REFERENCES organizations (id)
        ON DELETE RESTRICT,
    CONSTRAINT organization_products_product_fk FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT
);

COMMIT;
