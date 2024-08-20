-- Task 1: How many stores does the business have and in which countries?

SELECT * FROM dim_store_details
LIMIT 10;

SELECT country_code AS country, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC;

-- Task 2: Which locations currently have the most stores?

SELECT locality, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

-- Task 3: Which months produced the largest amount of sales?

SELECT 
    SUM(dim_orders.product_quantity * dim_products.product_price_gbp) AS total_sales,
    EXTRACT(MONTH FROM dim_date_times.datetime) AS month
FROM 
    dim_orders
JOIN 
    dim_date_times ON dim_orders.date_uuid = dim_date_times.date_uuid
JOIN 
    dim_products ON dim_orders.product_code = dim_products.product_code
GROUP BY 
    month
ORDER BY 
    total_sales DESC
LIMIT 6;

-- Task 4: How many sales are coming from online?

SELECT 
    COUNT(dim_orders.store_code) AS numbers_of_sales,
    SUM(dim_orders.product_quantity) AS product_quantity_count,
    'Web' AS location
FROM 
    dim_orders
JOIN 
    dim_store_details ON dim_orders.store_code = dim_store_details.store_code
WHERE 
    dim_store_details.store_code LIKE 'WEB%'
GROUP BY 
    location

UNION

SELECT 
    COUNT(dim_orders.store_code) AS numbers_of_sales,
    SUM(dim_orders.product_quantity) AS product_quantity_count,
    'Offline' AS location
FROM 
    dim_orders
JOIN 
    dim_store_details ON dim_orders.store_code = dim_store_details.store_code
WHERE 
    dim_store_details.store_code NOT LIKE 'WEB%'
GROUP BY 
    location;

-- Task 5: What percentage of sales come through each type of store?

SELECT 
    dim_store_details.store_type,
    SUM(dim_orders.product_quantity * dim_products.product_price_gbp) AS total_sales,
    (SUM(dim_orders.product_quantity * dim_products.product_price_gbp) / 
        (SELECT SUM(dim_orders.product_quantity * dim_products.product_price_gbp)::numeric 
         FROM dim_orders 
         JOIN dim_products ON dim_orders.product_code = dim_products.product_code) * 100) AS percentage_total
FROM 
    dim_orders
JOIN 
    dim_store_details ON dim_orders.store_code = dim_store_details.store_code
JOIN 
    dim_products ON dim_orders.product_code = dim_products.product_code
GROUP BY 
    dim_store_details.store_type
ORDER BY 
    total_sales DESC;

-- Task 6: Which month in each year produced the highest cost of sales?

WITH monthly_sales AS (
    SELECT
        SUM(dim_orders.product_quantity * dim_products.product_price_gbp) AS total_sales,
        EXTRACT(YEAR FROM dim_date_times.datetime) AS year,
        EXTRACT(MONTH FROM dim_date_times.datetime) AS month
    FROM 
        dim_orders
    JOIN 
        dim_date_times ON dim_orders.date_uuid = dim_date_times.date_uuid
    JOIN 
        dim_products ON dim_orders.product_code = dim_products.product_code
    GROUP BY 
        year, month
),
ranked_sales AS (
    SELECT 
        total_sales,
        year,
        month,
        RANK() OVER (PARTITION BY year ORDER BY total_sales DESC) AS sales_rank
    FROM 
        monthly_sales
)
SELECT 
    total_sales,
    year,
    month
FROM 
    ranked_sales
WHERE 
    sales_rank = 1
ORDER BY 
    total_sales DESC
LIMIT 9;

-- Task 7: What is our staff headcount?

SELECT 
    country_code, 
    SUM(staff_numbers) AS total_staff_numbers
FROM 
    dim_store_details
WHERE 
    staff_numbers IS NOT NULL
GROUP BY 
    country_code
ORDER BY 
    total_staff_numbers DESC;

-- Task 8: Which German store type is selling the most?

SELECT
    SUM(dim_orders.product_quantity * dim_products.product_price_gbp) AS total_sales,
    dim_store_details.store_type,
    dim_store_details.country_code
FROM
    dim_orders
JOIN
    dim_store_details ON dim_orders.store_code = dim_store_details.store_code
JOIN
    dim_products ON dim_orders.product_code = dim_products.product_code
WHERE
    dim_store_details.country_code = 'DE'
GROUP BY
    dim_store_details.store_type,
    dim_store_details.country_code
ORDER BY
    total_sales DESC;

-- Task 9: How quickly is the company making sales?

WITH sales_with_next_sale AS (
    SELECT
        date_part('year', dim_date_times.datetime) AS year,
        dim_date_times.datetime AS current_sale,
        LEAD(dim_date_times.datetime) OVER (ORDER BY dim_date_times.datetime) AS next_sale
    FROM
        dim_orders
    JOIN
        dim_date_times ON dim_orders.date_uuid = dim_date_times.date_uuid
)
SELECT
    year,
    AVG(next_sale - current_sale) AS average_time_between_sales
FROM
    sales_with_next_sale
WHERE
    next_sale IS NOT NULL
GROUP BY
    year
ORDER BY
    average_time_between_sales ASC;




