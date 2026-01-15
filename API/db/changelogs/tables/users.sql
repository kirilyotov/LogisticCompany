--liquibase formatted sql

--changeset ${AUTHOR_NAME}:1.5_create_users_table
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid(),
    company_id UUID,
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role user_role NOT NULL DEFAULT 'client',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT fk_users_company FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL
);

COMMENT ON TABLE users IS 'Unified user table. Clients may or may not be linked to a specific company.';
COMMENT ON COLUMN users.company_id IS 'The company this user belongs to. NULL for Super Admins.';
COMMENT ON COLUMN users.role IS 'Access level: super_admin, admin, employee, or client.';


CREATE INDEX idx_users_company ON users(company_id);

--rollback DROP TABLE users;
