ALTER TABLE dim_orders
ALTER COLUMN date_uuid SET DATA TYPE UUID USING date_uuid::UUID;

ALTER TABLE dim_orders
ALTER COLUMN user_uuid SET DATA TYPE UUID USING user_uuid::UUID;

SELECT MAX(LENGTH(CAST(card_number AS VARCHAR))) FROM dim_orders;

SELECT MAX(LENGTH(store_code)) FROM dim_orders;

SELECT MAX(LENGTH(product_code)) FROM dim_orders;

ALTER TABLE dim_orders
ALTER COLUMN card_number SET DATA TYPE VARCHAR(19);

ALTER TABLE dim_orders
ALTER COLUMN store_code SET DATA TYPE VARCHAR(12);

ALTER TABLE dim_orders
ALTER COLUMN product_code SET DATA TYPE VARCHAR(11);

ALTER TABLE dim_orders
ALTER COLUMN product_quantity SET DATA TYPE SMALLINT;

SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'dim_orders';

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_users';

SELECT MAX(LENGTH(country_code)) FROM dim_users;

ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN country_code TYPE VARCHAR(2),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_store_details';

SELECT MAX(LENGTH(store_code)) FROM dim_store_details;
SELECT MAX(LENGTH(country_code)) FROM dim_store_details;

SELECT *
FROM dim_store_details
WHERE (LENGTH(store_code) = 10 AND store_code ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(country_code) = 10 AND country_code ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(continent) = 10 AND continent ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(latitude::text) = 10 AND latitude::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(longitude::text) = 10 AND longitude::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(locality) = 10 AND locality ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(staff_numbers::text) = 10 AND staff_numbers::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(opening_date::text) = 10 AND opening_date::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(store_type) = 10 AND store_type ~ '^[A-Z0-9]{10}$');

DELETE FROM dim_store_details
WHERE (LENGTH(store_code) = 10 AND store_code ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(country_code) = 10 AND country_code ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(continent) = 10 AND continent ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(latitude::text) = 10 AND latitude::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(longitude::text) = 10 AND longitude::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(locality) = 10 AND locality ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(staff_numbers::text) = 10 AND staff_numbers::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(opening_date::text) = 10 AND opening_date::text ~ '^[A-Z0-9]{10}$')
   OR (LENGTH(store_type) = 10 AND store_type ~ '^[A-Z0-9]{10}$');

ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(11),
    ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
    ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT,
    ALTER COLUMN country_code TYPE VARCHAR(2),
    ALTER COLUMN continent TYPE VARCHAR(255);

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dim_products';

SELECT * FROM dim_products
LIMIT 10;

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(20);

UPDATE dim_products
SET weight_class = CASE
    WHEN weight_kg < 2 THEN 'Light'
    WHEN weight_kg >= 2 AND weight_kg < 40 THEN 'Mid_Sized'
    WHEN weight_kg >= 40 AND weight_kg < 140 THEN 'Heavy'
    WHEN weight_kg >= 140 THEN 'Truck_Required'
    ELSE 'Unknown'
END;

DELETE FROM dim_products
WHERE product_name IS NULL 
AND product_price_gbp IS NULL 
AND category IS NULL 
AND date_added IS NULL;

SELECT MAX(LENGTH("EAN")) FROM dim_products;
SELECT MAX(LENGTH(product_code)) FROM dim_products;
SELECT MAX(LENGTH(weight_class)) FROM dim_products;

-- Rename the column
ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;



-- Change the data types
ALTER TABLE dim_products
	ALTER COLUMN product_price_gbp TYPE FLOAT USING product_price_gbp::FLOAT,
	ALTER COLUMN weight_kg TYPE FLOAT USING weight_kg::FLOAT,
	ALTER COLUMN "EAN" TYPE VARCHAR(17) USING "EAN"::VARCHAR(17),
	ALTER COLUMN product_code TYPE VARCHAR(11) USING product_code::VARCHAR(11),
	ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
	ALTER COLUMN "uuid" TYPE UUID USING "uuid"::UUID,
	ALTER COLUMN still_available TYPE BOOLEAN USING CASE WHEN still_available = 'true' THEN true ELSE false END,
	ALTER COLUMN weight_class TYPE VARCHAR(14) USING weight_class::VARCHAR(14);

SELECT * FROM dim_date_times
LIMIT 10;

SELECT MAX(LENGTH(time_period)) FROM dim_date_times;

ALTER TABLE dim_date_times
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
	ALTER COLUMN time_period TYPE VARCHAR(10) USING time_period::VARCHAR(10);

SELECT * FROM dim_store_details
LIMIT 10;

SELECT MAX(LENGTH(card_number)) FROM dim_card_details;
SELECT MAX(LENGTH(expiry_date)) FROM dim_card_details;

ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(19) USING card_number::VARCHAR(19),
	ALTER COLUMN expiry_date TYPE VARCHAR(5) USING expiry_date::VARCHAR(5),
	ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;

SELECT * FROM dim_date_times
LIMIT 10;

SELECT user_uuid, COUNT(*) FROM dim_users GROUP BY user_uuid HAVING COUNT(*) > 1;
SELECT user_uuid, COUNT(*) FROM dim_users GROUP BY user_uuid HAVING COUNT(*) > 1;
SELECT store_code, COUNT(*) FROM dim_store_details GROUP BY store_code HAVING COUNT(*) > 1;
SELECT card_number, COUNT(*) FROM dim_card_details GROUP BY card_number HAVING COUNT(*) > 1;
SELECT date_uuid, COUNT(*) FROM dim_date_times GROUP BY date_uuid HAVING COUNT(*) > 1;

-- Remove rows with NULL values in user_uuid column in dim_users
DELETE FROM dim_users WHERE user_uuid IS NULL;

-- Remove rows with NULL values in product_code column in dim_products
DELETE FROM dim_products WHERE product_code IS NULL;

-- Remove rows with NULL values in store_code column in dim_store_details
DELETE FROM dim_store_details WHERE store_code IS NULL;

-- Remove rows with NULL values in card_number column in dim_card_details
DELETE FROM dim_card_details WHERE card_number IS NULL;

-- Remove rows with NULL values in date_uuid column in dim_date_times
DELETE FROM dim_date_times WHERE date_uuid IS NULL;


-- Alter tables to add primary key constraints
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);

ALTER TABLE dim_orders
ADD CONSTRAINT fk_date_uuid
FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);

ALTER TABLE dim_orders
ADD CONSTRAINT fk_user_uuid
FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);

ALTER TABLE dim_orders
ADD CONSTRAINT fk_card_number
FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

ALTER TABLE dim_orders
ADD CONSTRAINT fk_store_code
FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);

ALTER TABLE dim_orders
ADD CONSTRAINT fk_product_code
FOREIGN KEY (product_code) REFERENCES dim_products(product_code);

SELECT DISTINCT store_code
FROM dim_orders
WHERE store_code NOT IN (SELECT store_code FROM dim_store_details);

DELETE FROM dim_orders
WHERE store_code NOT IN (SELECT store_code FROM dim_store_details);

SELECT * FROM dim_orders
LIMIT 10;

SELECT
    tc.table_schema,
    tc.table_name,
    kcu.column_name,
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu 
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu 
      ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='dim_orders';
