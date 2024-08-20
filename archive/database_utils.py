import yaml
from sqlalchemy import create_engine, inspect
import pandas as pd
from typing import Optional, Dict


class DatabaseConnector:
    def __init__(self, config_path: str = 'db_creds.yaml'):
        self.config = self._read_db_creds(config_path)
        self.engine = self._init_db_engine()

    def _read_db_creds(self, path: str) -> Optional[Dict[str, str]]:
        """Read database credentials from a YAML file and return as a dictionary."""
        try:
            with open(path, 'r') as file:
                creds = yaml.safe_load(file)
            return creds
        except FileNotFoundError:
            print(f"Error: The file {path} was not found.")
            return None
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            return None

    def _init_db_engine(self) -> Optional[create_engine]:
        """Initialize and return an SQLAlchemy database engine using the credentials."""
        if not self.config:
            print("No configuration available.")
            return None

        try:
            db_url = (
                f"postgresql://{self.config['RDS_USER']}:{self.config['RDS_PASSWORD']}"
                f"@{self.config['RDS_HOST']}:{self.config['RDS_PORT']}/{self.config['RDS_DATABASE']}"
            )
            engine = create_engine(db_url)
            print("Database engine initialized successfully.")
            return engine
        except KeyError as e:
            print(f"Missing key in database credentials: {e}")
            return None
        except Exception as e:
            print(f"Error initializing database engine: {e}")
            return None

    def list_db_tables(self) -> Optional[list]:
        """List all tables in the database."""
        if not self.engine:
            print("Database engine is not initialized.")
            return None

        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            print("Tables in the database:", tables)
            return tables
        except Exception as e:
            print(f"Error listing tables: {e}")
            return None

    def upload_to_db(self, df: pd.DataFrame, table_name: str):
        """Upload a DataFrame to the specified table in the database."""
        if not self.engine:
            print("Database engine is not initialized.")
            return

        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"Data uploaded to table {table_name} successfully.")
        except Exception as e:
            print(f"Error uploading data to table {table_name}: {e}")


if __name__ == "__main__":
    # Example usage of DatabaseConnector
    db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

    # List all tables in the database
    tables = db_connector.list_db_tables()

    # Example DataFrame to upload
    data = {'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']}
    df = pd.DataFrame(data)

    # Upload DataFrame to the database
    if tables:
        db_connector.upload_to_db(df, 'example_table')
