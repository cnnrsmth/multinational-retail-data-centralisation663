from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def main():
    # Step 1: Define API details
    stores_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
    store_details_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details"
    headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}

    # Step 2: Create an instance of DataExtractor
    data_extractor = DataExtractor()

    # Step 3: Retrieve the number of stores
    number_of_stores = data_extractor.list_number_of_stores(stores_endpoint, headers)
    print(f"Number of stores: {number_of_stores}")

    if number_of_stores:
        # Step 4: Retrieve stores data
        stores_df = data_extractor.retrieve_stores_data(store_details_endpoint, headers, number_of_stores)
        print("Data before cleaning:")
        print(stores_df.head())  # Display the first few rows of the stores DataFrame

        # Step 5: Clean the Data
        data_cleaner = DataCleaning()
        cleaned_df = data_cleaner.clean_store_details(stores_df)

        # Step 6: Display the cleaned data
        print("Data after cleaning:")
        print(cleaned_df.head())

        # Step 7: Connect to the Local Database
        local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

        # Step 8: Upload the cleaned data to the local database as 'dim_store_details'
        local_db_connector.upload_to_db(cleaned_df, "dim_store_details")
    else:
        print("Failed to retrieve number of stores.")

if __name__ == "__main__":
    main()
