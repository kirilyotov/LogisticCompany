--liquibase formatted sql
--changeset ${AUTHOR_NAME}:1.9_shipment_history_trigger splitStatements:false runOnChange:true
DROP TRIGGER IF EXISTS trg_shipment_history_audit ON shipments;
CREATE TRIGGER trg_shipment_history_audit
AFTER INSERT OR UPDATE OF current_status ON shipments
FOR EACH ROW
EXECUTE FUNCTION fn_log_status_change();
--rollback DROP TRIGGER IF EXISTS trg_shipment_history_audit ON shipments;