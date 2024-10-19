import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_project(base_name, version="v1"):
    """
    Creates a project folder for storing model training results and sets environment variables.

    Parameters:
    - base_name (str): The user-provided base name for the folder.
    - version (str): The version of the training, defaults to 'v1'.

    Returns:
    - main_dir (str): Path to the main directory where all results are stored.
    """
    # Load global environment variables from .env 
    load_dotenv()

    # Generate the datetime string
    current_time = datetime.now().strftime('%Y-%m-%d')

    # Create the main directory name
    main_dir = f"{base_name}_{version}_{current_time}"

    # Create the directory structure
    os.makedirs(main_dir, exist_ok=True)

    # Subfolders for organization
    subfolders = ["charts", "data", "models", "pipeline", "logs"]

    # Prepare content for the .env_temp file
    env_content = f"PROJECT_DIR={main_dir}\n"

    for subfolder in subfolders:
        folder_path = os.path.join(main_dir, subfolder)
        os.makedirs(folder_path, exist_ok=True)

        # Set environment variable for the subfolder
        env_var_name = f"{subfolder.upper()}_DIR"
        os.environ[env_var_name] = folder_path

        # Add to .env_temp content
        env_content += f"{env_var_name}={folder_path}\n"

        print(f"Set environment variable: {env_var_name}={folder_path}")

    # Write the environment variables to .env_temp in the project directory
    env_temp_path = os.path.join(main_dir, ".env_temp")
    with open(env_temp_path, "w") as f:
        f.write(env_content)

    print(f".env_temp file created at: {env_temp_path}")

    # Set environment variable for the main directory
    os.environ["PROJECT_DIR"] = main_dir
    print(f"Set environment variable: PROJECT_DIR={main_dir}")

    return main_dir


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def filetype(file):
    """
    This function is for manually loading small datasets. The file type must be a .csv
    or one of the listed Excel formats.

    Parameters:
    - file(str): The file path to the data.

    Returns:
    - DataFrame if successful, None if an error occurs.
    """
    try:
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith(('.xls', '.xlsx', '.odf', '.ods', '.odt')):  
            df = pd.read_excel(file)
        else:
            print(f'Error: The file {file} has an unsupported format.')
            return None

    except ValueError as ve:
        print(f"Warning: {ve}. The file will be loaded without 'datetime' parsing.")
        
        if file.endswith('.csv'):
            df = pd.read_csv(file)  
        elif file.endswith(('.xls', '.xlsx', '.odf', '.ods', '.odt')):  
            df = pd.read_excel(file)  
        else:
            print(f'Error: The file {file} has an unsupported format.')
            return None

    except FileNotFoundError:
        print(f"FileNotFoundError: The file {file} was not found.")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return df


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def save_data(df, filename, filepath, xlsx=False):
    """
    Saves a DataFrame to a file either as a CSV or an Excel file.
    
    Parameters:
    - df (pandas.DataFrame): The DataFrame to save.
    - filename (str): The base name of the file.
    - filepath (str): The directory path where the file will be saved.
    - xlsx (bool): Optional; if True, the DataFrame will be saved as an Excel file. 
                 If False, it will be saved as a CSV file. Default is False.
    
    Returns:
    None

    Raises:
    - Exception: Outputs an error message if the DataFrame could not be saved.
    """
    full_path = os.path.join(filepath, filename)

    if df.empty:
        print("Warning: The DataFrame is empty. No file will be saved.")
        return

    try:
        if xlsx:
            full_path += '.xlsx'
            df.to_excel(full_path)
        else:
            full_path += '.csv'
            df.to_csv(full_path)
        print(f"File saved successfully at {full_path}")
    except Exception as e:
        print(f"Failed to save the file at {full_path}. Error: {e}")


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def save_groups(df, column, file_path):
    """
    Groups a DataFrame by a specified column and saves each group to a separate .csv file.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to be grouped.
        column (str): The column name to group by.
        file_path (str): The directory where the .csv files will be saved.
    """
    # Ensure the file path exists, if not, create it
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # Group the DataFrame by the specified column
    grouped = df.groupby(column)

    # Iterate over each group and save to a .csv file
    for group_name, group_df in grouped:
        group_name = str(group_name).replace(" ", "_")
        
        # Construct the file name using the group name
        file_name = f"{group_name}.csv"
        full_path = os.path.join(file_path, file_name)
        
        # Save the group to a .csv file
        group_df.to_csv(full_path, index=False)

    print(f"Files saved to: {file_path}")


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_table(table_name, conn):
    """
    Checks if a table exists in PostgreSQL. If not, creates the table with schema.
    """
    table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        date DATE,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        Adj_Close FLOAT,
        Volume BIGINT,
        sentiment_score FLOAT,
        sentiment_count INT
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(table_query)
            conn.commit()
            print(f"Table '{table_name}' is ready.")
    except Exception as e:
        conn.rollback()
        print(f"Error ensuring table exists: {e}")
    finally:
        cur.close()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def df_to_postgres(df, table_name, conn, batch_size=1000):
    """
    Inserts a Pandas DataFrame into a PostgreSQL table.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data to be inserted.
        table_name (str): The name of the PostgreSQL table.
        conn (psycopg2.connection): Active PostgreSQL connection object.
        batch_size (int): Number of rows to insert per batch.
    """
    # make sure the table is there
    check_table(table_name, conn)

    # Generate the column names
    columns = ', '.join(df.columns)

    # Generate the placeholder
    placeholders = ', '.join(['%s'] * len(df.columns))

    # Build the SQL INSERT statement
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Convert the DataFrame
    data_tuples = [tuple(row) for row in df.to_numpy()]

    try:
        with conn.cursor() as cur:
            for i in range(0, len(data_tuples), batch_size):
                batch = data_tuples[i:i + batch_size]
                cur.executemany(insert_query, batch)
                conn.commit()
                print(f"Inserted batch {i // batch_size + 1} successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()

