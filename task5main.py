from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def main():
    # Step 1: Connect to the AWS RDS Database
    rds_db_connector = DatabaseConnector(config_path='aws_db_creds.yaml')

    # Step 2: Extract Data from RDS
    data_extractor = DataExtractor(rds_db_connector)
    orders_df = data_extractor.read_rds_table('orders_table')
    print("Data before cleaning:")
    print(orders_df.head())  # Display the first few rows of the orders DataFrame

    # Step 3: Clean the Data
    data_cleaner = DataCleaning()
    cleaned_df = data_cleaner.clean_orders_data(orders_df)
    print("Data after cleaning:")
    print(cleaned_df.head())

    # Step 4: Connect to the Local Database
    local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

    # Step 5: Upload the cleaned data to the local database as 'dim_orders'
    local_db_connector.upload_to_db(cleaned_df, "dim_orders")

if __name__ == "__main__":
    main()
