from database_utils import DatabaseConnector
from data_cleaning import DataCleaning

def main():
    # Step 1: Fetch the JSON data from the S3 URL and save it to a file
    json_url = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
    filename = "date_details.json"

    data_cleaner = DataCleaning()
    raw_json_data = data_cleaner.fetch_and_save_json(json_url, filename)

    if raw_json_data:
        # Step 2: Clean the saved JSON file
        cleaned_df = data_cleaner.clean_date_events_data(raw_json_data)

        if cleaned_df is not None:
            print("Final cleaned data:")
            print(cleaned_df.head())

            # Step 3: Connect to the Local Database
            local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

            # Step 4: Upload the cleaned data to the local database as 'dim_date_events'
            local_db_connector.upload_to_db(cleaned_df, "dim_date_times")

if __name__ == "__main__":
    main()
