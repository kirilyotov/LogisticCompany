--liquibase formatted sql

--changeset ${AUTHOR_NAME}:1.6_create_shipments_table
CREATE TABLE shipments (
    id UUID DEFAULT gen_random_uuid(),
    tracking_number SERIAL,
    company_id UUID NOT NULL,
    sender_id UUID NOT NULL,
    receiver_id UUID NOT NULL,
    origin_office_id UUID,
    destination_office_id UUID,
    delivery_address TEXT,
    weight DECIMAL(10, 2) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_to_office BOOLEAN DEFAULT TRUE,
    current_status shipment_status DEFAULT 'created',
    created_by UUID,
    last_modified_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_shipments PRIMARY KEY (id),
    CONSTRAINT fk_shipments_company FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT fk_shipments_sender FOREIGN KEY (sender_id) REFERENCES users(id),
    CONSTRAINT fk_shipments_receiver FOREIGN KEY (receiver_id) REFERENCES users(id),
    CONSTRAINT fk_shipments_origin_office FOREIGN KEY (origin_office_id) REFERENCES offices(id),
    CONSTRAINT fk_shipments_dest_office FOREIGN KEY (destination_office_id) REFERENCES offices(id),
    CONSTRAINT fk_shipments_creator FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT fk_shipments_modifier FOREIGN KEY (last_modified_by) REFERENCES users(id)
);

COMMENT ON TABLE shipments IS 'Primary ledger of all parcel deliveries.';
COMMENT ON COLUMN shipments.tracking_number IS 'Human-readable tracking ID.';
COMMENT ON COLUMN shipments.is_to_office IS 'If true, delivery is to office. If false, to address.';
COMMENT ON COLUMN shipments.price IS 'Total delivery cost.';
COMMENT ON COLUMN shipments.last_modified_by IS 'User who last changed the status or details.';


CREATE INDEX IF NOT EXISTS idx_shipments_company ON shipments(company_id);
CREATE INDEX IF NOT EXISTS idx_shipments_sender ON shipments(sender_id);
CREATE INDEX IF NOT EXISTS idx_shipments_receiver ON shipments(receiver_id);
CREATE INDEX IF NOT EXISTS idx_shipments_date ON shipments(created_at);

--rollback DROP TABLE shipments;