import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def format_date(df):
    """
    Rename and standardize date column, convert them to datetime,
    and strip the time component.
    
    Parameters:
    - df: The DataFrame to process.
    
    Returns:
    - Processed DataFrame with standardized 'date' column, or None if an error occurs.
    """
    try:
        # Identify columns that are like 'Date', 'date', 'datetime'
        date_columns = [col for col in df.columns if col.lower() in ['date', 'datetime']]
        
        # date column exists
        if not date_columns:
            raise KeyError("No 'date' or 'datetime' column found in the DataFrame.")
        
        # Rename them all to 'date'
        for col in date_columns:
            df.rename(columns={col: 'date'}, inplace=True)
        
        # Convert 'date' column to datetime and strip the time component
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
        
        # Check for errors
        if df['date'].isnull().all():
            raise ValueError("The 'date' column could not be converted to valid dates.")
    
    except KeyError as e:
        print(f"KeyError: {e}")
        return None
    
    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
    return df

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def aggregate_column(df, agg_columns):
    """
    Aggregate dataframe by the date column.

    Parameters:
    - df: The DataFrame to aggregate.
    - agg_columns: A dictionary where the keys are column names and the values are aggregation functions.

    Returns:
    - Aggregated DataFrame or None if an error occurs.
    """
    try:
        # Ensure 'date' column exists
        if 'date' not in df.columns:
            raise KeyError("The DataFrame does not contain a 'date' column.")

        # Ensure 'date' column is in datetime format and strip the time part
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

        if df['date'].isnull().all():
            raise ValueError("The 'date' column could not be converted to datetime.")

        # Check if columns exist
        missing_cols = [col for col in agg_columns.keys() if col not in df.columns]
        if missing_cols:
            raise KeyError(f"The following columns are missing from the DataFrame: {missing_cols}")

        # Aggregate columns based on the dictionary
        aggregated_df = df.groupby('date').agg(agg_columns).reset_index()

    except KeyError as e:
        print(f"KeyError: {e}")
        return None

    except ValueError as e:
        print(f"ValueError: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return aggregated_df
