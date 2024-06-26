from database_utils import DatabaseConnector
from sqlalchemy import text
import pandas as pd
import tabula
import requests

class DataExtractor:
    def __init__(self, db_connector=None):
        self.db_connector = db_connector

    def list_tables(self):
        """List all tables in the database using the DatabaseConnector."""
        if self.db_connector:
            return self.db_connector.list_db_tables()
        else:
            print("No database connection provided.")
            return None

    def read_data(self, table_name):
        """Read data from the specified table and return it as a list of dictionaries."""
        if self.db_connector:
            try:
                with self.db_connector.engine.connect() as connection:
                    query = text(f"SELECT * FROM {table_name}")
                    result = connection.execute(query)
                    data = [dict(row) for row in result.mappings()]
                    return data
            except Exception as e:
                print(f"Error reading data from table {table_name}: {e}")
                return None
        else:
            print("No database connection provided.")
            return None
        
    def read_rds_table(self, table_name):
        """Read a table from the RDS database into a pandas DataFrame."""
        if self.db_connector:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, self.db_connector.engine)
                return df
            except Exception as e:
                print(f"Error reading table {table_name}: {e}")
                return None
        else:
            print("No database connection provided.")
            return None
        
    def retrieve_pdf_data(self, link):
        """
        Retrieve data from a PDF document and return it as a pandas DataFrame.
        """
        try:
            # Extract data from the PDF file
            df_list = tabula.read_pdf(link, pages='all', multiple_tables=True)

            # Combine all the tables into a single DataFrame
            df = pd.concat(df_list, ignore_index=True)
            return df
        except Exception as e:
            print(f"Error retrieving data from PDF: {e}")
            return None

    def list_number_of_stores(self, stores_endpoint, headers):
        """
        Retrieve the number of stores from the API.
        """
        try:
            response = requests.get(stores_endpoint, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data['number_stores']
            else:
                print(f"Failed to retrieve number of stores. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving number of stores: {e}")
            return None

    def retrieve_stores_data(self, store_endpoint, headers, number_of_stores):
        """
        Retrieve the details of all stores from the API and return as a pandas DataFrame.
        """
        stores_data = []
        for store_number in range(1, number_of_stores):
            try:
                response = requests.get(f"{store_endpoint}/{store_number}", headers=headers)
                if response.status_code == 200:
                    store_data = response.json()
                    stores_data.append(store_data)
                else:
                    print(f"Failed to retrieve data for store number {store_number}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error retrieving data for store number {store_number}: {e}")
        
        return pd.DataFrame(stores_data)


if __name__ == "__main__":
    # API details
    stores_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
    store_details_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details"
    headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}

    # Create an instance of DataExtractor
    data_extractor = DataExtractor()

    # List number of stores
    number_of_stores = data_extractor.list_number_of_stores(stores_endpoint, headers)
    print(f"Number of stores: {number_of_stores}")

    if number_of_stores:
        # Retrieve stores data
        stores_df = data_extractor.retrieve_stores_data(store_details_endpoint, headers, number_of_stores)
        print(stores_df.head())  # Display the first few rows of the stores DataFrame