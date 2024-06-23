import yaml
from sqlalchemy import create_engine, inspect, text

class DatabaseConnector:
    def __init__(self, config_path='db_creds.yaml'):
        self.config = self.read_db_creds(config_path)
        self.engine = self.init_db_engine()

    def read_db_creds(self, path):
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
        
    def init_db_engine(self):
        """Initialize and return an SQLAlchemy database engine using the credentials."""
        if not self.config:
            print("No configuration available.")
            return None
        
        try:
            # Construct the database URL
            db_url = (
                f"postgresql://{self.config['RDS_USER']}:{self.config['RDS_PASSWORD']}"
                f"@{self.config['RDS_HOST']}:{self.config['RDS_PORT']}/{self.config['RDS_DATABASE']}"
            )
            # Create the SQLAlchemy engine
            engine = create_engine(db_url)
            print("Database engine initialized successfully.")
            return engine
        except KeyError as e:
            print(f"Missing key in database credentials: {e}")
            return None
        except Exception as e:
            print(f"Error initializing database engine: {e}")
            return None

    def list_db_tables(self):
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

# Usage example
if __name__ == "__main__":
    db_connector = DatabaseConnector()
    print(db_connector)
    engine = db_connector.engine
    print(engine)
