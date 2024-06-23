import pandas as pd
import numpy as np
import re

class DataCleaning:
    def __init__(self):
        pass

    def clean_address(self, df):
        """
        Clean the address column by removing newline characters.
        """
        df['address'] = df['address'].str.replace('\n', ',')
        return df
    
    def merge_latitude_columns(self, df):
        """
        Merge 'lat' and 'latitude' columns into a single column.
        Prioritize 'latitude' values over 'lat' if both are present.
        """
        # If 'latitude' is missing, fill it with 'lat' values
        df['latitude'] = df['latitude'].combine_first(df['lat'])
        # Drop the 'lat' column
        df.drop(columns=['lat'], inplace=True)
        return df
    
    def convert_data_types(self, df):
        """
        Convert data types of appropriate columns.
        """
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        return df
    
    def clean_opening_date(self, df):
        """
        Clean the opening_date column by handling non-standard date formats and converting errors to NaN.
        """
        def parse_non_standard_dates(date_str):
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
            
        # Apply custom parsing to the non-standard dates
        df['opening_date'] = df['opening_date'].apply(lambda x: parse_non_standard_dates(x) if pd.isna(pd.to_datetime(x, errors='coerce')) else pd.to_datetime(x, errors='coerce'))

        return df
    
    def clean_categorical_columns(self, df):
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
    
    def clean_locality(self, df):
        """
        Clean the locality column by ensuring it does not contain any numbers.
        """
        df['locality'] = df['locality'].apply(lambda x: x if (isinstance(x, str) and not any(char.isdigit() for char in x)) else np.nan)
        return df

    def clean_store_code(self, df):
        """
        Clean the store_code column by ensuring it contains a '-' separator.
        """
        df['store_code'] = df['store_code'].apply(lambda x: x if (isinstance(x, str) and '-' in x) else np.nan)
        return df
    
    def clean_staff_numbers(self, df):
        """
        Clean the staff_numbers column by converting all values to numeric, coercing errors to NaN.
        """
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        return df
    
    def standardize_nulls(self, df):
        """
        Standardize different representations of null values to np.nan.
        """
        null_representations = ['NULL', 'None', 'N/A', '']
        df.replace(null_representations, np.nan, inplace=True)
        
        df = df.where(pd.notnull(df), np.nan)
        return df
    


