--liquibase formatted sql

--changeset ${AUTHOR_NAME}:1.4_create_offices_table
CREATE TABLE offices (
    id UUID DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    country_code VARCHAR(2) NOT NULL DEFAULT 'BG',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_offices PRIMARY KEY (id),
    CONSTRAINT fk_offices_company FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

COMMENT ON TABLE offices IS 'Locations where packages can be sent from or delivered to.';
COMMENT ON COLUMN offices.company_id IS 'The owner company of this office.';

CREATE INDEX idx_offices_company ON offices(company_id);
