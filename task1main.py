from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def main():
    # Step 1: Connect to the RDS Database
    rds_db_connector = DatabaseConnector(config_path='db_creds.yaml')

    # Step 2: Extract Data from RDS
    data_extractor = DataExtractor(rds_db_connector)
    tables = data_extractor.list_tables()

    # Specify the table you want to clean
    target_table = 'legacy_users'

    if target_table in tables:
        df = data_extractor.read_rds_table(target_table)
        if df is not None:
            print("Data before cleaning:")
            print(df.head())  # Display the first few rows of the DataFrame

            # Step 3: Clean the Data
            data_cleaner = DataCleaning()
            cleaned_df = data_cleaner.clean_user_data(df)
            print("Data after cleaning:")
            print(cleaned_df.head())  # Display the first few rows of the cleaned DataFrame

            # Step 4: Connect to the Local Database
            local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

            # Step 5: Upload the cleaned data to the local database as 'dim_users'
            local_db_connector.upload_to_db(cleaned_df, "dim_users")
    else:
        print(f"Table {target_table} not found in the database.")

if __name__ == "__main__":
    main()
