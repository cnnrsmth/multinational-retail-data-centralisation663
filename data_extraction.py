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

    def extract_rds_table(self, table_name: str) -> pd.DataFrame:
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
        try:
            df_list = tabula.read_pdf(link, pages='all', multiple_tables=True)
            df = pd.concat(df_list, ignore_index=True)
            return df
        except Exception as e:
            print(f"Error retrieving data from PDF: {e}")
            return pd.DataFrame()

    def list_number_of_stores(self, stores_endpoint: str, headers: dict) -> int:
        try:
            response = requests.get(stores_endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get('number_stores', 0)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving number of stores: {e}")
            return 0

    def retrieve_stores_data(self, store_endpoint: str, headers: dict, number_of_stores: int) -> pd.DataFrame:
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
        bucket_name = s3_uri.split('/')[2]
        s3_file_key = '/'.join(s3_uri.split('/')[3:])
        return bucket_name, s3_file_key
