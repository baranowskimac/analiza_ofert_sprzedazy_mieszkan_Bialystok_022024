from datetime import datetime, timezone
import os
import pickle


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