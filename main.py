from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from data_loading import DataLoader

def main():
    # Initialize database connectors
    rds_db_connector = DatabaseConnector(config_path='aws_db_creds.yaml')
    local_db_connector = DatabaseConnector(config_path='local_db_creds.yaml')

    # Initialize data extractor, cleaner, and loader
    data_extractor = DataExtractor(db_connector=rds_db_connector)
    data_cleaner = DataCleaning()
    data_loader = DataLoader(db_connector=local_db_connector)

    # Example: Process User Data
    user_df = data_extractor.extract_rds_table('legacy_users')
    cleaned_user_df = data_cleaner.clean_data(user_df, 'user')
    data_loader.load_to_db(cleaned_user_df, 'dim_users')

    # Example: Process Card Data
    card_df = data_extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
    cleaned_card_df = data_cleaner.clean_data(card_df, 'card')
    data_loader.load_to_db(cleaned_card_df, 'dim_card_details')

    # Example: Process Store Data
    number_of_stores = data_extractor.list_number_of_stores(
        stores_endpoint="https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores",
        headers={"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
    )
    stores_df = data_extractor.retrieve_stores_data(
        store_endpoint="https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details",
        headers={"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"},
        number_of_stores=number_of_stores
    )
    cleaned_stores_df = data_cleaner.clean_data(stores_df, 'store')
    data_loader.load_to_db(cleaned_stores_df, 'dim_store_details')

    # Example: Process Product Data
    product_df = data_extractor.extract_from_s3('s3://data-handling-public/products.csv')
    cleaned_product_df = data_cleaner.clean_data(product_df, 'product')
    data_loader.load_to_db(cleaned_product_df, 'dim_products')

    # Example: Process Orders Data
    orders_df = data_extractor.extract_rds_table('orders_table')
    cleaned_orders_df = data_cleaner.clean_data(orders_df, 'order')
    data_loader.load_to_db(cleaned_orders_df, 'dim_orders')

    # Example: Process Date Events Data
    date_events_df = data_extractor.extract_json_from_url('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json')
    cleaned_date_events_df = data_cleaner.clean_data(date_events_df, 'date_event')
    data_loader.load_to_db(cleaned_date_events_df, 'dim_date_times')

if __name__ == "__main__":
    main()
