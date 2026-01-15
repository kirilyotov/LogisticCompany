--liquibase formatted sql
--changeset ${AUTHOR_NAME}:1.0_create_enums splitStatements:false
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('super_admin', 'admin', 'employee', 'client');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'shipment_status') THEN
        CREATE TYPE shipment_status AS ENUM (
            'created', 'pending', 'sent', 'in_transit',
            'arrived_at_office', 'out_for_delivery', 'delivered', 'collected'
        );
    END IF;
END $$;
--rollback DROP TYPE IF EXISTS shipment_status; DROP TYPE IF EXISTS user_role;