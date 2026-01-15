--liquibase formatted sql

--changeset ${AUTHOR_NAME}:2.2_initial_demo_data_v3 context:dev splitStatements:false
DO $$
DECLARE
    v_company_speedy_id UUID;
    v_company_econt_id UUID;
    v_company_dhl_id UUID;

    v_office_sofia_id UUID;
    v_office_plovdiv_id UUID;
    v_office_varna_id UUID;
    v_office_burgas_id UUID;
    v_office_airport_id UUID;

    v_user_super_admin_id UUID;
    v_user_speedy_admin_id UUID;
    v_user_speedy_driver_id UUID;
    v_user_econt_admin_id UUID;
    v_user_econt_driver_id UUID;
    v_user_dhl_admin_id UUID;

    v_user_client_sender_id UUID;
    v_user_client_receiver_id UUID;

    v_shipment_id UUID;

    -- Valid bcrypt hash for 'password123'
    v_password_hash TEXT := '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J.fGqGZ9y';
BEGIN
    -- 0. Create Super Admin
    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (NULL, 'super@logistics.com', v_password_hash, 'Super', 'Admin', 'super_admin')
    RETURNING id INTO v_user_super_admin_id;

    -- 1. Create Companies
    -- Company 1: Speedy
    INSERT INTO companies (name, vat_number)
    VALUES ('Speedy Logistics', 'BG123456789')
    RETURNING id INTO v_company_speedy_id;

    -- Company 2: Econt
    INSERT INTO companies (name, vat_number)
    VALUES ('Econt Express', 'BG987654321')
    RETURNING id INTO v_company_econt_id;

    -- Company 3: DHL
    INSERT INTO companies (name, vat_number)
    VALUES ('DHL Bulgaria', 'BG112233445')
    RETURNING id INTO v_company_dhl_id;

    -- 2. Create Offices
    -- Speedy Offices
    INSERT INTO offices (company_id, name, address, city, country_code)
    VALUES (v_company_speedy_id, 'Sofia HQ', '1 Tsarigradsko Shose', 'Sofia', 'BG')
    RETURNING id INTO v_office_sofia_id;

    INSERT INTO offices (company_id, name, address, city, country_code)
    VALUES (v_company_speedy_id, 'Plovdiv Hub', '55 Maritsa Blvd', 'Plovdiv', 'BG')
    RETURNING id INTO v_office_plovdiv_id;

    -- Econt Offices
    INSERT INTO offices (company_id, name, address, city, country_code)
    VALUES (v_company_econt_id, 'Varna Central', '10 Vladislav Varnenchik', 'Varna', 'BG')
    RETURNING id INTO v_office_varna_id;

    INSERT INTO offices (company_id, name, address, city, country_code)
    VALUES (v_company_econt_id, 'Burgas Plaza', '5 Transportna Str', 'Burgas', 'BG')
    RETURNING id INTO v_office_burgas_id;

    -- DHL Offices
    INSERT INTO offices (company_id, name, address, city, country_code)
    VALUES (v_company_dhl_id, 'Sofia Airport Hub', 'Brussels Blvd', 'Sofia', 'BG')
    RETURNING id INTO v_office_airport_id;

    -- 3. Create Users
    -- Speedy Staff
    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_speedy_id, 'admin@speedy.com', v_password_hash, 'Speedy', 'Admin', 'admin')
    RETURNING id INTO v_user_speedy_admin_id;

    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_speedy_id, 'driver@speedy.com', v_password_hash, 'John', 'Driver', 'employee')
    RETURNING id INTO v_user_speedy_driver_id;

    -- Econt Staff
    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_econt_id, 'admin@econt.com', v_password_hash, 'Econt', 'Admin', 'admin')
    RETURNING id INTO v_user_econt_admin_id;

    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_econt_id, 'courier@econt.com', v_password_hash, 'Ivan', 'Courier', 'employee')
    RETURNING id INTO v_user_econt_driver_id;

    -- DHL Staff
    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_dhl_id, 'admin@dhl.com', v_password_hash, 'DHL', 'Manager', 'admin')
    RETURNING id INTO v_user_dhl_admin_id;

    -- Clients (Assigned to Speedy)
    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_speedy_id, 'sender@gmail.com', v_password_hash, 'Alice', 'Sender', 'client')
    RETURNING id INTO v_user_client_sender_id;

    INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
    VALUES (v_company_speedy_id, 'receiver@gmail.com', v_password_hash, 'Bob', 'Receiver', 'client')
    RETURNING id INTO v_user_client_receiver_id;

    -- 4. Create Shipments

    -- Shipment 1: Speedy (Created)
    -- Insert as 'created'. Trigger uses created_by.
    INSERT INTO shipments (
        company_id, sender_id, receiver_id, origin_office_id, destination_office_id,
        weight, price, is_to_office, current_status, created_by
    )
    VALUES (
        v_company_speedy_id, v_user_client_sender_id, v_user_client_receiver_id, v_office_sofia_id, v_office_plovdiv_id,
        2.5, 15.00, TRUE, 'created', v_user_speedy_admin_id
    );

    -- Shipment 2: Speedy (Delivered with history)
    -- 1. Create
    INSERT INTO shipments (
        company_id, sender_id, receiver_id, origin_office_id, destination_office_id,
        delivery_address, weight, price, is_to_office, current_status, created_by
    )
    VALUES (
        v_company_speedy_id, v_user_client_sender_id, v_user_client_receiver_id, v_office_sofia_id, NULL,
        'Some Street 123', 5.0, 25.00, FALSE, 'created', v_user_speedy_admin_id
    )
    RETURNING id INTO v_shipment_id;

    -- 2. Update to 'sent' (by driver)
    UPDATE shipments
    SET current_status = 'sent',
        last_modified_by = v_user_speedy_driver_id,
        updated_at = NOW()
    WHERE id = v_shipment_id;

    -- 3. Update to 'delivered' (by driver)
    UPDATE shipments
    SET current_status = 'delivered',
        last_modified_by = v_user_speedy_driver_id,
        updated_at = NOW()
    WHERE id = v_shipment_id;


    -- Shipment 3: Econt (In Transit)
    DECLARE
        v_user_econt_sender_id UUID;
    BEGIN
        INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
        VALUES (v_company_econt_id, 'sender_econt@gmail.com', v_password_hash, 'Eve', 'EcontSender', 'client')
        RETURNING id INTO v_user_econt_sender_id;

        -- 1. Create
        INSERT INTO shipments (
            company_id, sender_id, receiver_id, origin_office_id, destination_office_id,
            weight, price, is_to_office, current_status, created_by
        )
        VALUES (
            v_company_econt_id, v_user_econt_sender_id, v_user_econt_sender_id, v_office_varna_id, v_office_burgas_id,
            1.0, 10.00, TRUE, 'created', v_user_econt_admin_id
        )
        RETURNING id INTO v_shipment_id;

        -- 2. Update to 'in_transit' (by driver)
        UPDATE shipments
        SET current_status = 'in_transit',
            last_modified_by = v_user_econt_driver_id,
            updated_at = NOW()
        WHERE id = v_shipment_id;
    END;

    -- Shipment 4: DHL (Pending)
    DECLARE
        v_user_dhl_sender_id UUID;
    BEGIN
        INSERT INTO users (company_id, email, password_hash, first_name, last_name, role)
        VALUES (v_company_dhl_id, 'sender_dhl@gmail.com', v_password_hash, 'Dave', 'DhlSender', 'client')
        RETURNING id INTO v_user_dhl_sender_id;

        -- Insert as 'pending' directly (assuming it starts as pending)
        INSERT INTO shipments (
            company_id, sender_id, receiver_id, origin_office_id, destination_office_id,
            delivery_address, weight, price, is_to_office, current_status, created_by
        )
        VALUES (
            v_company_dhl_id, v_user_dhl_sender_id, v_user_dhl_sender_id, v_office_airport_id, NULL,
            'International St 99', 10.0, 100.00, FALSE, 'pending', v_user_dhl_admin_id
        );
    END;

END $$;
