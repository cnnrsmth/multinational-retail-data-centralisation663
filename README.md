# Multinational Retail Data Centralisation

The Sales Data Centralization Project focuses on consolidating data from various sources into a centralized PostgreSQL database, ensuring data is accessible, reliable, and ready for analysis. This project entails setting up a database, extracting and cleaning data from multiple sources, and performing queries to generate insights for business decision-making.

## Table of Contents

- [Architecture Overview](#Architecture-Overview)
- [Milestone 1: Environment Setup](#Milestone-1-Environment-Setup)
- [Milestone 2: Data Extraction and Cleaning](#Milestone-2-Data-Extraction-and-Cleaning)
- [Milestone 3: Data Schema and Database Setup](#Milestone-3-Data-Schema-and-Database-Setup)
- [Milestone 4: Data Querying and Analysis](#Milestone-4-Data-Querying-and-Analysis)
- [Conclusion](#Conclusion)

## Architecture Overview

The architecture for this project involves:

- **Data Sources**: Various data sources, including CSV files from S3, JSON files, PDF documents, and data from AWS RDS.
- **Data Processing**: Python scripts for data extraction, cleaning, and transformation.
- **Database**: A PostgreSQL database set up in pgAdmin4 to store centralized data.
- **Analysis**: SQL queries to analyze the data stored in the centralized database.

## Milestone 1: Environment Setup

### Task 1: Database Setup

**Goal**: Initialize a new PostgreSQL database in pgAdmin4 to store extracted data.
**Steps:**

- Create a new database named sales_data.
- Define schemas and create tables for user, product, store, card details, and order data.
- Ensure the database is ready to store the cleaned data extracted from various sources.

### Task 2: Script Initialization

**Goal**: Set up the foundational scripts needed for data extraction, cleaning, and database interaction.
**Steps:**

- Create a Python script data_extraction.py with a DataExtractor class to handle data extraction from CSV, JSON, PDF, and API sources.
- Develop a script database_utils.py containing a DatabaseConnector class to manage database connections and uploads.
- Create a data_cleaning.py script with a DataCleaning class to clean and preprocess data before it is stored in the database.

## Milestone 2: Data Extraction and Cleaning

### Task 1: Database Setup

**Goal**: Create and initialize a local database to store the extracted data.
**Steps:**

- Set up a PostgreSQL database named sales_data in pgAdmin4.
- Define and create tables for storing the extracted data, including dim_users, dim_card_details, dim_store_details, dim_products, orders_table, and dim_date_times.

### Task 2: Script Initialization

**Goal**: Initialize the scripts and classes that will be used to extract and clean data from multiple data sources.
**Steps:**

- Create data_extraction.py with a DataExtractor class to handle extraction from CSV files, APIs, and S3 buckets.
- Develop database_utils.py with a DatabaseConnector class for database interactions.
- Implement data_cleaning.py with a DataCleaning class for data preprocessing and cleaning.

### Task 3: Extract and Clean User Data

**Goal**: Extract historical user data from an AWS RDS database, clean it, and store it in the dim_users table.
**Steps:**

- **Extract** Use the DataExtractor class to connect to the RDS instance and extract the user data.
- **Clean**: Implement clean_user_data method in DataCleaning class to address null values, date errors, and data type inconsistencies.
- **Store**: Upload the cleaned data to the PostgreSQL database using the DatabaseConnector class.

### Task 4: Extract and Clean Card Details

**Goal**: Extract and clean card details from a PDF document stored in an AWS S3 bucket.
**Steps:**

- **Extract**: Utilize retrieve_pdf_data in DataExtractor to extract data from the PDF.
- **Clean**: Use clean_card_data in DataCleaning to remove null values, correct formatting issues, and ensure consistency.
- **Store**: Upload the cleaned data to the dim_card_details table in the PostgreSQL database.

### Task 5: Extract and Clean Store Data

**Goal**: Extract store details via an API, clean the data, and upload it to the dim_store_details table.
**Steps:**

- **Extract**: Use list_number_of_stores and retrieve_stores_data methods in DataExtractor to extract store data via API.
- **Clean**: Implement clean_store_data in DataCleaning to handle inconsistencies in country codes, address formatting, and date formats.
- **Store**: Upload cleaned data to the PostgreSQL database using upload_to_db method.

### Task 6: Extract and Clean Product Data

**Goal**: Extract product details from a CSV in an S3 bucket, clean the data, and store it in the dim_products table.
**Steps:**

- **Extract**: Use extract_from_s3 in DataExtractor to download and read the CSV file.
- **Clean**: Implement methods in DataCleaning to convert inconsistent weight units, remove unnecessary characters, and clean product prices.
- **Store**: Upload the cleaned data to the PostgreSQL database using the DatabaseConnector class.

### Task 7: Extract and Clean Orders Data

**Goal**: Extract orders data from AWS RDS, clean it, and store it in the orders_table.
**Steps:**

- **Extract**: Use the read_rds_table method in DataExtractor to fetch orders data.
- **Clean**: Implement clean_orders_data in DataCleaning to remove unnecessary columns and ensure consistency across the dataset.
- **Store**: Upload the cleaned data to the PostgreSQL database.

### Task 8: Extract and Clean Date Events Data

**Goal**: Extract date events data from a JSON file on S3, clean it, and store it in dim_date_times.
**Steps:**

- **Extract**: Use extract_json_from_s3 in DataExtractor to read the JSON file.
- **Clean**: Implement clean_events_data in DataCleaning to ensure the timestamp and time period data is correctly formatted.
- **Store**: Upload the cleaned data to the PostgreSQL database.

## Milestone 3: Data Schema and Database Setup

### Task 1: Correct Data Types

**Goal**: Ensure all columns in the database have the correct data types, facilitating efficient queries and accurate data representation.
**Steps:**

- Review current data types and compare them against the requirements.
- Update data types in the PostgreSQL database using SQL commands, ensuring consistency across all tables.

### Task 2: Set Primary and Foreign Keys

**Goal**: Establish relationships between tables using primary and foreign keys, creating a star schema.
**Steps:**

- Set primary keys in dim_users, dim_products, dim_store_details, and other dimension tables.
- Define foreign keys in orders_table to reference primary keys in dimension tables, ensuring referential integrity.

## Milestone 4: Data Querying and Analysis

### Task 1: Country and Store Analysis

**Goal**: Determine which countries have the most stores and provide insights into store distribution.
**Steps:**

- Execute SQL queries to count stores per country and identify the country with the highest number of stores.
- Visualize the results using tools like pgAdmin4's query editor or external data visualization

### Task 2: Sales Analysis

**Goal**: Analyze monthly sales to identify trends, including the most successful months.
**Steps:**

- Write SQL queries to calculate the total sales per month by multiplying product price with quantity.
- Aggregate the sales data by month and year to identify peak sales periods.
- Visualize trends in monthly sales, focusing on key metrics like total revenue and sales volume.

### Task 3: Store Type Revenue Analysis

**Goal**: Determine the revenue contribution of each store type to optimize focus areas.
**Steps:**

- Create SQL queries to group sales data by store type (e.g., physical stores, online).
- Calculate the percentage of total sales each store type contributes.
- Analyze the data to identify which store types generate the most revenue and strategize accordingly.

### Task 4: Staff Numbers Analysis

**Goal**: Assess the distribution of staff numbers across different regions to optimize resource allocation.
**Steps:**

- Write SQL queries to sum up staff numbers across different countries and regions.
- Group the data by continent and country to compare staffing levels.
- Use the analysis to make informed decisions on staffing needs and regional resource allocation.

### Task 5: German Store Type Performance

**Goal**: Identify the most successful store types in Germany to guide expansion strategies.
**Steps:**

- Execute SQL queries to filter sales data specifically for German stores.
- Group the data by store type and calculate the total sales per type.
- Analyze which store type is the most profitable, providing insights for expansion.

### Task 6: Sales Speed Analysis

**Goal**: Calculate the average time between sales to gauge sales velocity over the years.
**Steps:**

- Use SQL queries to calculate the time difference between consecutive sales.
- Group the results by year to analyze changes in sales speed over time.
- Use the findings to assess how sales strategies have impacted transaction speed and customer engagement.

## Conclusion

The Sales Data Centralization Project successfully consolidated multiple data sources into a centralized PostgreSQL database. Through extensive data extraction, cleaning, and transformation processes, the project set up a robust database schema to support detailed analysis. The resulting insights into sales trends, store performance, and staff distribution provide valuable information to drive data-informed business decisions.
