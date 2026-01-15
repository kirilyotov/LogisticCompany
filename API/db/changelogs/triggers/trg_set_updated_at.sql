--liquibase formatted sql

--changeset your_name:1.8_shipments_updated_at_trigger runOnChange:true splitStatements:false
--comment: Attaches the timestamp trigger

-- Companies
DROP TRIGGER IF EXISTS trg_companies_upd ON companies;
CREATE TRIGGER trg_companies_upd BEFORE UPDATE ON companies
FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION fn_set_updated_at();

-- Users
DROP TRIGGER IF EXISTS trg_users_upd ON users;
CREATE TRIGGER trg_users_upd BEFORE UPDATE ON users
FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION fn_set_updated_at();

-- Offices
DROP TRIGGER IF EXISTS trg_offices_upd ON offices;
CREATE TRIGGER trg_offices_upd BEFORE UPDATE ON offices
FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION fn_set_updated_at();

-- Shipments
DROP TRIGGER IF EXISTS trg_shipments_set_updated_at ON shipments;
CREATE TRIGGER trg_shipments_set_updated_at BEFORE UPDATE ON shipments
FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION fn_set_updated_at();

--rollback DROP TRIGGER IF EXISTS trg_companies_upd ON companies;
--rollback DROP TRIGGER IF EXISTS trg_users_upd ON users;
--rollback DROP TRIGGER IF EXISTS trg_offices_upd ON offices;
--rollback DROP TRIGGER IF EXISTS trg_shipments_upd ON shipments;