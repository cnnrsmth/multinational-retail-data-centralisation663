from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def main():
    # Step 1: Retrieve data from the PDF
    pdf_link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    data_extractor = DataExtractor()
    pdf_data_df = data_extractor.retrieve_pdf_data(pdf_link)

    if pdf_data_df is not None:
        print("Data before cleaning:")
        print(pdf_data_df.head())  # Display the first few rows of the DataFrame

        # Step 2: Clean the Data
        data_cleaner = DataCleaning()
        
        # Step-by-step cleaning process
        cleaned_df = data_cleaner.standardize_nulls(pdf_data_df)
        print("Data after standardizing nulls:")
        print(cleaned_df.head())

        cleaned_df = data_cleaner.clean_card_number(cleaned_df)
        print("Data after cleaning card numbers:")
        print(cleaned_df.head())

        cleaned_df = data_cleaner.clean_dates(cleaned_df, date_columns=['date_payment_confirmed'])
        print("Data after cleaning dates:")
        print(cleaned_df.head())

        cleaned_df = data_cleaner.remove_invalid_rows(cleaned_df)
        print("Data after removing invalid rows:")
        print(cleaned_df.head())

        # Final cleaned data
        print("Final cleaned data:")
        print(cleaned_df.head())

        # Step 3: Connect to the Local Database
        local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

        # Step 4: Upload the cleaned data to the local database as 'dim_card_details'
        local_db_connector.upload_to_db(cleaned_df, "dim_card_details")
    else:
        print("Failed to retrieve data from the PDF.")

if __name__ == "__main__":
    main()
