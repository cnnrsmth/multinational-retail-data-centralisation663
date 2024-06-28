import pandas as pd
import requests
import tabula
import boto3
from sqlalchemy import text
from io import StringIO
from database_utils import DatabaseConnector


class DataExtractor:
    def __init__(self, db_connector: DatabaseConnector = None):
        self.db_connector = db_connector

    def list_tables(self) -> list:
        """List all tables in the database using the DatabaseConnector."""
        if self.db_connector:
            return self.db_connector.list_db_tables()
        else:
            print("No database connection provided.")
            return []

    def read_data(self, table_name: str) -> list:
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
                return []
        else:
            print("No database connection provided.")
            return []

    def read_rds_table(self, table_name: str) -> pd.DataFrame:
        """Read a table from the RDS database into a pandas DataFrame."""
        if self.db_connector:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, self.db_connector.engine)
                return df
            except Exception as e:
                print(f"Error reading table {table_name}: {e}")
                return pd.DataFrame()
        else:
            print("No database connection provided.")
            return pd.DataFrame()

    def retrieve_pdf_data(self, link: str) -> pd.DataFrame:
        """Retrieve data from a PDF document and return it as a pandas DataFrame."""
        try:
            df_list = tabula.read_pdf(link, pages='all', multiple_tables=True)
            df = pd.concat(df_list, ignore_index=True)
            return df
        except Exception as e:
            print(f"Error retrieving data from PDF: {e}")
            return pd.DataFrame()

    def list_number_of_stores(self, stores_endpoint: str, headers: dict) -> int:
        """Retrieve the number of stores from the API."""
        try:
            response = requests.get(stores_endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get('number_stores', 0)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving number of stores: {e}")
            return 0

    def retrieve_stores_data(self, store_endpoint: str, headers: dict, number_of_stores: int) -> pd.DataFrame:
        """Retrieve the details of all stores from the API and return as a pandas DataFrame."""
        stores_data = []
        for store_number in range(1, number_of_stores + 1):
            try:
                response = requests.get(f"{store_endpoint}/{store_number}", headers=headers)
                response.raise_for_status()
                store_data = response.json()
                stores_data.append(store_data)
            except requests.exceptions.RequestException as e:
                print(f"Error retrieving data for store number {store_number}: {e}")

        return pd.DataFrame(stores_data)

    def extract_from_s3(self, s3_uri: str) -> pd.DataFrame:
        """Extract data from S3 and return as a pandas DataFrame."""
        bucket_name, s3_file_key = self._parse_s3_uri(s3_uri)
        s3_client = boto3.client('s3')

        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=s3_file_key)
            csv_string = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_string))
            return df
        except boto3.exceptions.Boto3Error as e:
            print(f"Error extracting data from S3: {e}")
            return pd.DataFrame()

    def extract_json_from_url(self, url: str) -> pd.DataFrame:
        """Extract JSON data from a URL and return it as a pandas DataFrame."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            df = pd.json_normalize(json_data)
            return df
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from URL: {e}")
            return pd.DataFrame()

    @staticmethod
    def _parse_s3_uri(s3_uri: str) -> tuple:
        """Parse the S3 URI into bucket name and file key."""
        bucket_name = s3_uri.split('/')[2]
        s3_file_key = '/'.join(s3_uri.split('/')[3:])
        return bucket_name, s3_file_key


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
