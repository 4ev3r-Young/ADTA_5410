import os
import platform
import pandas as pd
from datetime import datetime
from tensorflow.config import list_physical_devices, set_visible_devices
# from tensorflow.config.experimental import VirtualDeviceConfiguration


def set_device(use_gpu=True):
    """
    Set the device based on the availability of GPU.
    
    Parameters:
    - use_gpu (bool): If True, attempt to set the GPU as the device. If False, set the CPU.
    
    Returns:
    - device (str): 'CPU' or 'GPU' based on the configuration.
    """
    if use_gpu and list_physical_devices('GPU'):
        # GPU is available 
        device = 'GPU'
        # set specific GPU configurations here 
        gpu_devices = list_physical_devices('GPU')
        if gpu_devices:
            set_visible_devices(gpu_devices[0], 'GPU')  # Use the first GPU
            # configure virtual GPUs if necessary
            # set_virtual_device_configuration(gpu_devices[0], [VirtualDeviceConfiguration(memory_limit=2048)])
    else:
        # Fallback to CPU if no GPU is available
        device = 'CPU'
        cpu_devices = list_physical_devices('CPU')
        if cpu_devices:
            set_visible_devices(cpu_devices[0], 'CPU')
    
    return device




def filetype(file):
    """
    This function is for manually loading small datasets. The file type must be a .csv
    or one of the listed Excel formats.

    Parameters:
    - file(str): The file path to the data.

    Returns:
    - DataFrame if successful, None if an error occurs. If the 'datetime' column 
      is missing, it still loads the file but prints a warning.
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


def correct_file_path(file_path):
    """
    Corrects the file path for compatibility with the operating system.
    
    This function detects the operating system, adjusts the file path using the correct directory separators,
    and returns the corrected path.

    Parameters:
    - file_path (str): The initial file path .

    Returns:
    - file_path (str): The corrected file path.
    """
    current_os = platform.system()

    if current_os == "Windows":
        corrected_path = file_path.replace('/', '\\')
    else:  
        corrected_path = file_path.replace('\\', '/')

    return os.path.normpath(corrected_path)


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


def create_project(base_name, version="v1"):
    """
    Creates a project folder for storing model training results.
    
    Parameters:
    - base_name (str): The user-provided base name for the folder.
    - version (str): The version of the training, defaults to 'v1'.
    
    Returns:
    - main_dir (str): Path to the main directory where all results are stored.
    """
    # Generate the datetime string
    current_time = datetime.now().strftime('%Y-%m-%d')
    
    # Create the main directory name
    main_dir = f"{base_name}_{version}_{current_time}"
    
    # Create the directory structure
    os.makedirs(main_dir, exist_ok=True)
    
    # Subfolders for organization
    subfolders = ["charts", "models", "pipeline", "logs"]
    
    for subfolder in subfolders:
        os.makedirs(os.path.join(main_dir, subfolder), exist_ok=True)
    
    print(f"Training directory created at: {main_dir}")
    
    return main_dir



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
        # Replace spaces with underscores in the group name
        group_name = str(group_name).replace(" ", "_")
        
        # Construct the file name using the group name
        file_name = f"{group_name}.csv"
        full_path = os.path.join(file_path, file_name)
        
        # Save the group to a .csv file
        group_df.to_csv(full_path, index=False)

    print(f"Files saved to: {file_path}")