from datetime import datetime, timezone
import pandas as pd
import yaml
import os
import pickle

def read_config(config_path: str):
    with open(config_path, "r") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content

def create_save_data_path(batch: bool):

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
        
def save_file(oto_file, oto_path):
    with open(oto_path, "wb") as p:
        pickle.dump(oto_file, p)
    print(f'data_saved: {oto_path}')

def extract_to_df(oto_data: list):
    return_df = []
    for i in range(len(oto_data)):
        one_df = pd.DataFrame.from_dict(oto_data[i], orient='columns')
        return_df.append(one_df)
    return_df = pd.concat(return_df).reset_index()
    return return_df

