from src.OtoData_download import *
from src.OtoData_extract import *
from src.OtoData_scraper import *
from src.OtoData_rs import *


if __name__ == "__main__":
    
    print("Initializing..")

    oto_dom_data = download_Oto_Data(
        query_ad_params_path = './config/query_params.yaml',
        scrape_params_path = './scraper/scraper.yaml',
        page_counter = 1
    )

    print('preparing data')
    return_df = extract_to_df(oto_dom_data)

    print('saving data')
    path_to_save_file = create_save_data_path(batch = False)
    save_file(oto_file = return_df, oto_path = path_to_save_file)

