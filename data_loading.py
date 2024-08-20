import pandas as pd
from database_utils import DatabaseConnector

class DataLoader:
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector

    def load_to_db(self, df: pd.DataFrame, table_name: str):
        """Load cleaned data into the specified database table."""
        if self.db_connector and not df.empty:
            try:
                self.db_connector.upload_to_db(df, table_name)
            except Exception as e:
                print(f"Error loading data to table {table_name}: {e}")
        else:
            print("No data to load or database connection not provided.")
