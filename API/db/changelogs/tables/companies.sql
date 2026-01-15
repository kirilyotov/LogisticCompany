--liquibase formatted sql

--changeset ${AUTHOR_NAME}:1.3_create_companies_table
CREATE TABLE companies (
    id UUID DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    vat_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_companies PRIMARY KEY (id),
    CONSTRAINT uq_companies_vat UNIQUE (vat_number)
);

COMMENT ON TABLE companies IS 'Stores the different logistics entities (tenants) using the platform.';
COMMENT ON COLUMN companies.id IS 'Unique identifier for the company.';
COMMENT ON COLUMN companies.name IS 'Registered name of the logistics company.';
COMMENT ON COLUMN companies.vat_number IS 'Tax identification number.';
