import pandas as pd
import numpy as np
import re

class DataCleaning:
    def __init__(self):
        pass

    def clean_user_data(self, df):
        """
        Clean user data by standardizing null values, cleaning addresses, countries, country codes,
        phone numbers, handling dates, and removing rows with invalid data.
        """
        df = self.standardize_nulls(df)
        df = self.clean_address(df)
        df = self.clean_country_columns(df)
        df = self.clean_phone_number(df)
        df = self.clean_dates(df)
        df = self.remove_invalid_rows(df)
        return df

    def standardize_nulls(self, df):
        """
        Standardize different representations of null values to np.nan.
        """
        null_representations = ['NULL', 'None', 'N/A', '']
        df.replace(null_representations, np.nan, inplace=True)
        df = df.where(pd.notnull(df), np.nan)
        return df

    def clean_address(self, df):
        """
        Clean the address column by removing newline characters.
        """
        df['address'] = df['address'].str.replace('\n', ',')
        return df

    def clean_country_columns(self, df):
        """
        Clean country and country_code columns by removing invalid entries.
        """
        df['country'] = df['country'].apply(lambda x: x if not any(char.isdigit() for char in str(x)) else np.nan)
        df['country_code'] = df['country_code'].apply(lambda x: x if (not any(char.isdigit() for char in str(x)) and len(str(x)) <= 3) else np.nan)
        df['country_code'] = df['country_code'].replace('GGB', 'GB')
        return df

    def clean_phone_number(self, df):
        """
        Clean the phone_number column by removing invalid characters and standardizing format.
        """
        df['phone_number'] = df['phone_number'].apply(lambda x: re.sub(r'\D', '', str(x)))
        return df

    def clean_dates(self, df):
        """
        Clean date columns by converting to datetime and handling non-standard formats.
        """
        date_columns = ['date_of_birth', 'join_date']

        for col in date_columns:
            df[col] = df[col].apply(lambda x: self.parse_non_standard_dates(x) if pd.isna(pd.to_datetime(x, errors='coerce')) else pd.to_datetime(x, errors='coerce'))

        return df

    def parse_non_standard_dates(self, date_str):
        try:
            if re.match(r'\b\w+ \d{4} \d{2}\b', date_str): 
                return pd.to_datetime(date_str, format='%B %Y %d', errors='coerce')
            elif re.match(r'\b\d{4}/\d{2}/\d{2}\b', date_str):  
                return pd.to_datetime(date_str, format='%Y/%m/%d', errors='coerce')
            elif re.match(r'\b\d{4} \w+ \d{2}\b', date_str):  
                return pd.to_datetime(date_str, format='%Y %B %d', errors='coerce')
            elif re.match(r'\b\w+ \d{4} \d{2}\b', date_str): 
                return pd.to_datetime(date_str, format='%B %Y %d', errors='coerce')
            elif re.match(r'\b\w+ \d{4} \d{2}\b', date_str):  
                return pd.to_datetime(date_str, format='%B %Y %d', errors='coerce')
            else:
                return pd.to_datetime(date_str, errors='coerce')  
        except Exception:
            return np.nan

    def remove_invalid_rows(self, df):
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
