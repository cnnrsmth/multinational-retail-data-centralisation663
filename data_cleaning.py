import pandas as pd
import numpy as np
import re
import json
import requests
from typing import List, Dict, Any

class DataCleaning:
    def __init__(self):
        pass

    def clean_user_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean user data by standardizing null values, cleaning addresses, countries, country codes,
        phone numbers, handling dates, and removing rows with invalid data.
        """
        df = self.standardize_nulls(df)
        df = self.clean_address(df)
        df = self.clean_country_columns(df)
        df = self.clean_phone_number(df)
        df = self.clean_dates(df, date_columns=['date_of_birth', 'join_date'])
        df = self.remove_invalid_rows(df)
        return df

    def clean_card_details(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean card data by standardizing null values, removing rows with invalid data.
        """
        df = self.standardize_nulls(df)
        df = self.clean_dates(df, date_columns=['date_payment_confirmed'])
        df = self.remove_invalid_rows(df)
        df = self.clean_card_number(df)
        return df

    def clean_store_details(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean store details through various operations
        """
        df = self.standardize_nulls(df)
        df = self.clean_address(df)
        df = self.merge_latitude_columns(df)
        df = self.clean_dates(df, date_columns=['opening_date'])
        df = self.clean_categorical_columns(df)
        df = self.clean_locality(df)
        df = self.clean_store_code(df)
        df = self.clean_staff_numbers(df)
        return df
    
    def clean_product_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean product data by processing the weight column and converting all weights to kg.
        """
        df = self.standardize_nulls(df)
        df = self.remove_invalid_rows(df)
        df = self.clean_weight_column(df)
        df['product_price'] = df['product_price'].str.replace('£', '')
        df = self.convert_data_types(df, ['product_price'])
        df.rename(columns={'product_price': 'product_price_gbp'}, inplace=True)
        df = self.clean_dates(df, date_columns=['date_added'])
        return df
        
    def clean_orders_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean product data by processing the weight column and converting all weights to kg.
        """
        df = self.standardize_nulls(df)
        df = self.remove_invalid_rows(df)
        columns_to_drop = ['first_name', 'last_name', '1']
        df = self.drop_columns(df, columns_to_drop)
        df = self.convert_data_types(df, ['product_quantity'])
        return df

    def clean_date_events_data(self, json_data: Dict[str, Any]) -> pd.DataFrame:
        """Clean the date events data by following the structured steps."""
        df = self.reformat_json_to_df(json_data)
        print("Data after reformatting to DataFrame:")
        print(df.head())

        df = self.remove_null_rows(df)
        print("Data after removing null rows:")
        print(df.head())

        df = self.remove_invalid_rows_date_events_data(df)
        print("Data after removing invalid rows:")
        print(df.head())

        try:
            df = self.combine_datetime_columns(df)
            print("Data after combining datetime columns:")
            print(df.head())
        except Exception as e:
            print(f"Error during combining datetime columns: {e}")
            return None

        return df

    def standardize_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize different representations of null values to np.nan.
        """
        null_representations = ['NULL', 'None', 'N/A', '']
        df.replace(null_representations, np.nan, inplace=True)
        df = df.where(pd.notnull(df), np.nan)
        return df

    def clean_address(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the address column by removing newline characters.
        """
        df['address'] = df['address'].str.replace('\n', ',')
        return df

    def clean_country_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean country and country_code columns by removing invalid entries.
        """
        df['country'] = df['country'].apply(lambda x: x if not any(char.isdigit() for char in str(x)) else np.nan)
        df['country_code'] = df['country_code'].apply(lambda x: x if (not any(char.isdigit() for char in str(x)) and len(str(x)) <= 3) else np.nan)
        df['country_code'] = df['country_code'].replace('GGB', 'GB')
        return df

    def clean_phone_number(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the phone_number column by removing invalid characters and standardizing format.
        """
        df['phone_number'] = df['phone_number'].apply(lambda x: re.sub(r'\D', '', str(x)))
        return df

    def clean_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """
        Clean date columns by converting to datetime and handling non-standard formats.
        """
        for col in date_columns:
            df[col] = df[col].apply(lambda x: self.parse_non_standard_dates(x) if pd.isna(pd.to_datetime(x, errors='coerce')) else pd.to_datetime(x, errors='coerce'))
        return df

    def parse_non_standard_dates(self, date_str: str) -> pd.Timestamp:
        try:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return pd.to_datetime(date_str, format='%Y-%m-%d')
            elif re.match(r'^\d{4}/\d{2}/\d{2}$', date_str):
                return pd.to_datetime(date_str, format='%Y/%m/%d')
            elif re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
                return pd.to_datetime(date_str, format='%d/%m/%Y')
            elif re.match(r'^\d{2}/\d{2}$', date_str):
                return pd.to_datetime(date_str, format='%m/%y')
            elif re.match(r'^\w+ \d{4} \d{2}$', date_str):
                return pd.to_datetime(date_str, format='%B %Y %d')
            elif re.match(r'^\d{4} \w+ \d{2}$', date_str):
                return pd.to_datetime(date_str, format='%Y %B %d')
            else:
                return pd.to_datetime(date_str, errors='coerce')
        except Exception:
            return np.nan

    def clean_card_number(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the card_number column by removing invalid characters.
        """
        df['card_number'] = df['card_number'].apply(lambda x: re.sub(r'\?', '', str(x)) if isinstance(x, str) else x)
        return df

    def remove_invalid_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows with invalid data patterns.
        """
        def is_invalid_pattern(val):
            if isinstance(val, str) and len(val) == 10 and val.isalnum() and not val.isdigit() and not val.isalpha():
                return True
            return False

        # Check each row for invalid patterns
        invalid_rows = df.apply(lambda row: any(is_invalid_pattern(val) for val in row), axis=1)

        # Remove rows with invalid data
        df = df[~invalid_rows]

        return df

    def remove_invalid_rows_date_events_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove rows with invalid data patterns."""
        def is_invalid_pattern(val):
            if isinstance(val, str) and len(val) == 10 and val.isalnum() and not val.isdigit() and not val.isalpha():
                return True
            return False

        invalid_rows = df.apply(lambda row: any(is_invalid_pattern(val) for val in row), axis=1)
        df = df[~invalid_rows]
        return df

    def merge_latitude_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge 'lat' and 'latitude' columns into a single column.
        Prioritize 'latitude' values over 'lat' if both are present.
        """
        # If 'latitude' is missing, fill it with 'lat' values
        df['latitude'] = df['latitude'].combine_first(df['lat'])
        # Drop the 'lat' column
        df.drop(columns=['lat'], inplace=True)
        return df

    def convert_data_types(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Convert data types of specified columns to numeric.
        
        Parameters:
        df (pd.DataFrame): The DataFrame containing the columns to convert.
        columns (list): A list of column names to convert to numeric types.
        
        Returns:
        pd.DataFrame: The DataFrame with converted columns.
        """
        for column in columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        return df

    def clean_categorical_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean categorical columns: store_type, country_code, and continent.
        """
        # Clean store_type
        df['store_type'] = df['store_type'].apply(lambda x: x if not any(char.isdigit() for char in str(x)) else np.nan)

        # Clean country_code
        df['country_code'] = df['country_code'].apply(lambda x: x if (not any(char.isdigit() for char in str(x)) and len(str(x)) <= 3) else np.nan)

        # Clean continent
        df['continent'] = df['continent'].apply(lambda x: x.replace('ee', '') if isinstance(x, str) else x)
        df['continent'] = df['continent'].apply(lambda x: x if not any(char.isdigit() for char in str(x)) else np.nan)

        return df

    def clean_locality(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the locality column by ensuring it does not contain any numbers.
        """
        df['locality'] = df['locality'].apply(lambda x: x if (isinstance(x, str) and not any(char.isdigit() for char in x)) else np.nan)
        return df

    def clean_store_code(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the store_code column by ensuring it contains a '-' separator.
        """
        df['store_code'] = df['store_code'].apply(lambda x: x if (isinstance(x, str) and '-' in x) else np.nan)
        return df

    def clean_staff_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the staff_numbers column by converting all values to numeric, coercing errors to NaN.
        """
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        return df

    def clean_weight_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and convert the weight column to kilograms.
        """
        def extract_number_unit(s):
            if pd.isna(s):
                return [None, None]
            parts = re.split(r'(\d+\.?\d*)', s.replace(' ', ''))
            if len(parts) < 3:
                return [None, None]
            number = parts[1]
            unit = ''.join(parts[2:]).lower().strip()
            return [number, unit]

        def normalize_units(unit):
            if unit is None:
                return None
            unit = unit.lower().strip()
            if 'kg' in unit or 'kilogram' in unit:
                return 'kg'
            elif 'g' in unit or 'gram' in unit:
                return 'g'
            elif 'ml' in unit or 'milliliter' in unit or 'millilitre' in unit:
                return 'g'
            elif 'liter' in unit or 'liters' in unit or 'litre' in unit or 'litres' in unit:
                return 'liters'
            else:
                return None

        def convert_to_kilograms(row):
            try:
                number = float(row['number'])
                unit = row['unit']
                if unit == 'g':
                    return number / 1000  # Convert grams to kilograms
                elif unit == 'kg':
                    return number  # Already in kilograms
                elif unit == 'liters':
                    return number  # Assuming 1 liter = 1 kg
                else:
                    return None
            except (TypeError, ValueError):
                return None

        # Apply the extraction function to create separate number and unit columns
        df[['number', 'unit']] = df['weight'].apply(extract_number_unit).apply(pd.Series)

        # Normalize the units
        df['unit'] = df['unit'].apply(normalize_units)

        # Convert to kilograms
        df['weight_kg'] = df.apply(convert_to_kilograms, axis=1)

        # Drop the original weight, number, and unit columns
        df.drop(['weight', 'number', 'unit'], axis=1, inplace=True)

        return df

    def drop_columns(self, df: pd.DataFrame, columns_to_drop: List[str]) -> pd.DataFrame:
        """
        Drop specified columns from the DataFrame.
        """
        df = df.drop(columns=columns_to_drop, errors='ignore')
        return df

    def fetch_and_save_json(self, url: str, filename: str) -> Dict[str, Any]:
        """Fetch the JSON data from the given URL and save it to a file."""
        response = requests.get(url)
        raw_json_data = response.json()
        with open(filename, 'w') as f:
            json.dump(raw_json_data, f, indent=4)
        return raw_json_data

    def reformat_json_to_df(self, json_data: Dict[str, Any]) -> pd.DataFrame:
        """Reformat the JSON data to a structured DataFrame."""
        records = []
        for key in json_data['timestamp'].keys():
            record = {
                'timestamp': json_data['timestamp'][key],
                'month': json_data['month'][key],
                'year': json_data['year'][key],
                'day': json_data['day'][key],
                'time_period': json_data['time_period'][key],
                'date_uuid': json_data['date_uuid'][key]
            }
            records.append(record)
        df = pd.DataFrame(records)
        return df

    def remove_null_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove rows with null values in crucial columns."""
        df.replace('NULL', pd.NA, inplace=True)
        df.dropna(subset=['timestamp', 'day', 'month', 'year'], inplace=True)
        return df

    def combine_datetime_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Combine 'timestamp', 'day', 'month', and 'year' into a single datetime column."""
        df['datetime'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-' + df['day'].astype(str) + ' ' + df['timestamp'])
        df.drop(['timestamp', 'day', 'month', 'year'], axis=1, inplace=True)
        return df
