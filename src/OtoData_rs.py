from datetime import datetime, timezone
import pandas as pd
import yaml
import os
import pickle

def read_config(config_path: str) -> dict:

    """
    Function for loading congigs file

    Args:
        config_path (str): path to the config file

    Returns:
        dict: dict with attr items from a config file
    """

    with open(config_path, "r") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content

def create_save_data_path(batch: bool) -> str:

    """
    Function for create a dir & saving paths for save files

    Args:
        batch (bool): if directory for batch files should be created (True) or for full data set (False)

    Returns:
        str: path for saving files
    """

    tz = datetime.now(timezone.utc)
    tz_str = tz.strftime("%Y%m%d_%H%M%S")

    if batch == True:
        path = os.path.join(os.getcwd(), 'batch') 
        if not os.path.exists(path):
            os.mkdir(path)
        save_path = f'{path}/oto_dom_batch_{tz_str}.pkl'
    else:
        path = os.path.join(os.getcwd(), 'full_df')
        if not os.path.exists(path):
            os.mkdir(path)
        save_path = f'{path}/oto_dom_full_{tz_str}.pkl'

    return save_path
        
def save_file(
        oto_file, 
        oto_path: str
):
    
    """
    Function for saving files

    Args:
        oto_file: file for save (data frame, list, etc)
        oto_path (str): path where file should be saved
    """

    with open(oto_path, "wb") as p:
        pickle.dump(oto_file, p)
    print(f'data_saved: {oto_path}')



def extract_to_df(oto_data: list) -> pd.DataFrame:
    
    """
    Function for extracting list of list of dictionaries with ads scraped from oto dom data
    to easy and readable data frame format

    Args:
        oto_data (list): list with scraped data from oto dom service

    Returns:
        pd.DataFrame: readable data frame with data from oto dom service
    """
    
    return_df = []
    for i in range(len(oto_data)):
        one_df = pd.DataFrame.from_dict(oto_data[i], orient='columns')
        return_df.append(one_df)
    return_df = pd.concat(return_df).reset_index()
    return return_df

