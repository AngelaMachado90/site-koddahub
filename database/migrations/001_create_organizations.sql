-- ============================================================================
-- KODDAHUB — DATABASE MIGRATION
-- ============================================================================
--
-- Projeto     : Portal KoddaHub
-- Módulo      : Organizações / Clientes
-- Migration   : 001_create_organizations.sql
-- Versão      : 1.0.0
-- Data        : 2026-09-26
-- Responsável : Angela Natali Machado
-- Empresa     : KoddaHub
--
-- Objetivo:
-- Criar a entidade raiz de organizações do Portal KoddaHub.
-- A tabela representa empresas/clientes que poderão possuir usuários,
-- produtos contratados e chamados de suporte.
--
-- Escopo:
--   - Criar tabela organizations
--   - Definir chave primária
--   - Definir identificador técnico único (slug)
--   - Controlar status da organização
--   - Registrar timestamps de criação e atualização
--   - Aplicar constraints básicas de integridade
--
-- Fora de escopo:
--   - Usuários
--   - Autenticação
--   - Produtos
--   - Tickets
--   - Endereços e dados fiscais
--
-- Database     : koddahub_support
-- Owner/Role   : koddahub_support_app
-- PostgreSQL   : 16
--
-- Observações:
-- Esta migration deve ser executada exclusivamente no database
-- koddahub_support e utilizando a role apropriada da aplicação.
--
-- ============================================================================

BEGIN;

CREATE TABLE organizations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(160) NOT NULL,

    slug VARCHAR(160) NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT organizations_name_not_blank
        CHECK (btrim(name) <> ''),

    CONSTRAINT organizations_slug_not_blank
        CHECK (btrim(slug) <> ''),

    CONSTRAINT organizations_slug_format
        CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),

    CONSTRAINT organizations_status_valid
        CHECK (status IN ('active', 'inactive', 'suspended')),

    CONSTRAINT organizations_slug_unique
        UNIQUE (slug)
);

COMMIT;
