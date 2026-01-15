--liquibase formatted sql
--changeset your_name:1.1_fn_set_updated_at splitStatements:false runOnChange:true
CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--rollback DROP FUNCTION IF EXISTS fn_set_updated_at();