from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def main():
    # Step 1: S3 URI
    s3_uri = 's3://data-handling-public/products.csv'

    # Step 2: Create an instance of DataExtractor
    data_extractor = DataExtractor()

    # Step 3: Retrieve product data from S3
    products_df = data_extractor.extract_from_s3(s3_uri)
    print("Data before cleaning:")
    print(products_df.head())  # Display the first few rows of the products DataFrame

    # Step 4: Clean the Data
    data_cleaner = DataCleaning()
    cleaned_df = data_cleaner.clean_product_data(products_df)

    # Step 5: Display the cleaned data
    print("Data after cleaning:")
    print(cleaned_df.head())

    # Step 6: Connect to the Local Database
    local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

    # Step 7: Upload the cleaned data to the local database as 'dim_products'
    local_db_connector.upload_to_db(cleaned_df, "dim_products")

if __name__ == "__main__":
    main()
