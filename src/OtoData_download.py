from src.OtoData_scraper import *
from src.OtoData_rs import *

def download_Oto_Data(
        query_ad_params_path: str,
        scrape_params_path: str,
        headers_params_path: str
) -> list:
    
    """
    Function for downloading data from Oto Dom Service

    Args:
        query_params (dict): dictionary with params for looking for oto dom ads for scraping
        scrape_params_path (dict): dictionary with specific scrape params from a oto dom page
        page_counter (int): value of the next page (if there one than 1 page with ads)

    Returns:
        list: list with data about ads from Oto Dom service.
            One list element is one page with ads (specific ads in dict)
    """
    # read ad & scrape params from configs
    ad_params = read_config(query_ad_params_path)
    scrape_params = read_config(scrape_params_path)
    headers_params = read_config(headers_params_path)
    limit_ads_one_page = ad_params['limit']
     
    full_ds = []
    # page counter for changing url - if is more than one page of ads for scrape
    page_counter = ad_params['page_num']
    # while loop - works as as long as the number of ads on the page is less than the minimum required defined in the config
    while True:
    # return also n_url for checking how many ads it is on one page
        ads_data, n_urls = download_data(
             query_params = ad_params, 
             scrape_params = scrape_params,
             headers_params = headers_params, 
             page_counter=page_counter)
        
        path_to_save = create_save_data_path(batch = True)
        # sve batch files
        save_file(ads_data, path_to_save) 
        
        full_ds.append(ads_data)
        
        page_counter += 1
        # if n of urls is less than min defined ads in config - break a code. 
        # Means that there is no more ads for scrape!
        if n_urls < limit_ads_one_page:
            print('No More Data = stop downloading data')
            break
    
    return full_ds

