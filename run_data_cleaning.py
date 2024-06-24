from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
import pandas as pd

# Step 1: Connect to the Database
db_connector = DatabaseConnector()

# Step 2: Extract Data
data_extractor = DataExtractor(db_connector)
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

else:
    print(f"Table {target_table} not found in the database.")
