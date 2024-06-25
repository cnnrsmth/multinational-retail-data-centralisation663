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
        df = self.clean_dates(df, date_columns=['date_of_birth', 'join_date'])
        df = self.remove_invalid_rows(df)
        return df

    def clean_card_details(self, df):
        """
        Clean card data by standardizing null values, removing rows with invalid data.
        """  
        df = self.standardize_nulls(df)
        df = self.clean_dates(df, date_columns=['date_payment_confirmed'])
        df = self.remove_invalid_rows(df)
        df = self.clean_card_details(df)
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

    def clean_dates(self, df, date_columns):
        """
        Clean date columns by converting to datetime and handling non-standard formats.
        """

        for col in date_columns:
            df[col] = df[col].apply(lambda x: self.parse_non_standard_dates(x) if pd.isna(pd.to_datetime(x, errors='coerce')) else pd.to_datetime(x, errors='coerce'))

        return df

    def parse_non_standard_dates(self, date_str):
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
            elif re.match(r'^\d{4}/\d{2}/\d{2}$', date_str):
                return pd.to_datetime(date_str, format='%Y/%m/%d')
            elif re.match(r'^\w+ \d{4} \d{2}$', date_str):
                return pd.to_datetime(date_str, format='%B %Y %d')
            elif re.match(r'^\w+ \d{4} \d{2}$', date_str):
                return pd.to_datetime(date_str, format='%B %Y %d')
            else:
                return pd.to_datetime(date_str, errors='coerce')  
        except Exception:
            return np.nan
        
    
    def clean_card_number(self, df):
        """
        Clean the card_number column by removing invalid characters.
        """
        df['card_number'] = df['card_number'].apply(lambda x: re.sub(r'\?', '', str(x)) if isinstance(x, str) else x)
        return df

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
