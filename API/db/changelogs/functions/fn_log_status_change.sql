--liquibase formatted sql
--changeset ${AUTHOR_NAME}:1.2_fn_log_status_change splitStatements:false runOnChange:true
CREATE OR REPLACE FUNCTION fn_log_status_change()
RETURNS TRIGGER AS $$
DECLARE
    v_changed_by UUID;
BEGIN
    -- Determine who changed the status
    IF (TG_OP = 'INSERT') THEN
        v_changed_by := NEW.created_by;
    ELSE
        v_changed_by := NEW.last_modified_by;
    END IF;

    -- Only insert if the status has actually changed
    IF (TG_OP = 'INSERT') OR (OLD.current_status IS DISTINCT FROM NEW.current_status) THEN
        INSERT INTO shipment_status_history (
            shipment_id,
            status,
            changed_by,
            changed_at
        )
        VALUES (
            NEW.id,
            NEW.current_status,
            v_changed_by,
            CURRENT_TIMESTAMP
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--rollback DROP FUNCTION IF EXISTS fn_log_status_change();