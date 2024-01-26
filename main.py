from src.download_OtoData import *
from src.extract_ad_data import *
from src.otoDom_scraper import *
from src.save_OtoData import create_save_data_path, save_file


if __name__ == "__main__":
    
    print("Initializing..")

    oto_dom_data = download_Oto_Data(
        query_ad_params_path = './config/query_params.yaml',
        scrape_params_path = './scraper/scraper.yaml',
        page_counter = 1
    )

    print('saving data')
    path_to_save_file = create_save_data_path(batch = False)
    save_file(oto_dom_data, path_to_save_file)

