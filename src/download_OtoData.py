import yaml
from src.otoDom_scraper import *
from src.save_OtoData import create_save_data_path, save_file


def read_config(config_path: str):
    with open(config_path, "r") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content

def download_Oto_Data(
        query_ad_params_path: str,
        scrape_params_path: str,
        page_counter = 1
        ):
    
    """
        function for downloading data from Oto Dom Service

        Returns:
            pd.DataFrame: Data Frame with data about ads from Oto Dom service
    """
    ad_params = read_config(query_ad_params_path)
    scrape_params = read_config(scrape_params_path)
    limit_ads_one_page = ad_params['limit']
     
    full_ds = []

    page_counter = 1

    while True:
        ads_data, n_urls = download_data(
             query_params = ad_params, 
             scrape_params = scrape_params, 
             page_counter=page_counter)
        
        path_to_save = create_save_data_path(batch = True)
        save_file(ads_data, path_to_save)
        
        full_ds.append(ads_data)
        
        page_counter += 1
        
        if n_urls < limit_ads_one_page:
            print('No More Data = stop downloading data')
            break
    
    return full_ds

