--liquibase formatted sql
--changeset ${AUTHOR_NAME}:1.7_create_companies
-- SHIPMENT HISTORY
CREATE TABLE shipment_status_history (
    id UUID DEFAULT gen_random_uuid(),
    shipment_id UUID NOT NULL,
    status shipment_status NOT NULL,
    changed_by UUID,
    notes TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_shipment_history PRIMARY KEY (id),
    CONSTRAINT fk_history_shipment FOREIGN KEY (shipment_id) REFERENCES shipments(id) ON DELETE CASCADE,
    CONSTRAINT fk_history_user FOREIGN KEY (changed_by) REFERENCES users(id)
);

COMMENT ON TABLE shipment_status_history IS 'Log of every status change for every shipment.';

CREATE INDEX idx_history_shipment_lookup ON shipment_status_history(shipment_id, changed_at DESC);

--rollback DROP TABLE shipment_status_history;