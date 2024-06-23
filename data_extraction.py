from database_utils import DatabaseConnector
from sqlalchemy import text
import pandas as pd

class DataExtractor:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def list_tables(self):
        """List all tables in the database using the DatabaseConnector."""
        return self.db_connector.list_db_tables()

    def read_data(self, table_name):
        """Read data from the specified table and return it as a list of dictionaries."""
        try:
            with self.db_connector.engine.connect() as connection:
                # Perform a raw SQL query to read data
                query = text(f"SELECT * FROM {table_name}")
                result = connection.execute(query)
                data = [dict(row) for row in result.mappings()]
                return data
        except Exception as e:
            print(f"Error reading data from table {table_name}: {e}")
            return None
        
    def read_rds_table(self, table_name):
        """Read a table from the RDS database into a pandas DataFrame."""
        try:
            # Read the table into a DataFrame
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.db_connector.engine)
            return df
        except Exception as e:
            print(f"Error reading table {table_name}: {e}")
            return None

if __name__ == "__main__":
    db_connector = DatabaseConnector()
    data_extractor = DataExtractor(db_connector)

    # List tables
    tables = data_extractor.list_tables()
    print(tables)

    # Read data from a specific table (replace 'your_table' with an actual table name)
    if tables:
        table_name = tables[0]  # Example: read data from the first table  
        # Read table into a pandas DataFrame
        df = data_extractor.read_rds_table(table_name)
        if df is not None:
            print(df.head())  # Display the first few rows of the DataFrame
