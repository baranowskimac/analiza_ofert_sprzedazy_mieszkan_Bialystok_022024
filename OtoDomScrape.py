import json
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import date
import time


class scrape_otodom_data:

    """
        Object to extract all ads from a given page from OtoDom webservice
        
        Args:
            sprzedaz (str): define if it should be: sprzedaz / wynajem
            apartament_type: type of looked apartament. Possible types: miszkanie/kawalerka/dom/inwestycja/pokoj/dzialka/lokal/haleimagazyny/garaz
            region: cala-polska or one from voivodeship:
                dolnoslaskie
                kujawsko--pomorskie
                lodzkie
                lubelskie
                lubuskie
                malopolskie
                mazowieckie
                opolskie
                podkarpackie
                podlaskie
                pomorskie
                slaskie
                swietokrzyskie
                warminsko--mazurskie
                wielkopolskie
                zachodniopomorskie
            price_min (int): price min of looked apartament Default = None,
            price_max(int) = price max of looked apartament. Default = None,
            limit limit of ads on one page possible: 24, 36 48, 72
            page_counter: define a page number
            path_to_save_batch_files (str): path for saving batch files. Default is saving file in directory from scrip running
            path_to_save_full_files (str): path for saving fill data set file. Default is saving file in directory from scrip running
            sys_sleeping (int): System sleeping between loops. In seconds
    """

    def __init__(
            self, 
            sprzedaz = 'sprzedaz',
            apartament_type = 'mieszkanie',
            region = 'mazowieckie',
            limit  = '24',
            sys_sleeping = 1,  
            price_min = None, 
            price_max = None, 
            path_to_save_batch_files = None, 
            path_to_save_full_files = None):
        
        self.sprzedaz = sprzedaz
        self.apartament_type=apartament_type
        self.region = region
        self.price_min = price_min
        self.price_max = price_max
        self.limit = limit
        self.path_to_save_batch_files = path_to_save_batch_files
        self.path_to_save_full_files = path_to_save_full_files
        self.sys_sleeping = sys_sleeping


    def create_link_page_to_download(
            self,
            page_counter
    ):    
        """
        Function to extract all ads from a given page from OtoDom webservice
        Args:
        page_counter (int): value of the next page 
        Returns:
            page_url (str): url from Oto Dom service for downloading ads details
        """
        
        # create a link for downloading data
        main_page = 'https://www.otodom.pl/pl/wyniki'

        last_part_if_url = f'&ownerTypeSingleSelect=ALL&priceMin={self.price_min}&priceMax={self.price_max}&by=DEFAULT&direction=DESC&viewType=listing&page={page_counter}'
        
        page_url = f'{main_page}/{self.sprzedaz}/{self.apartament_type}/{self.region}?limit={self.limit}{last_part_if_url}'
        
        return page_url


    def define_page_to_extract(self, page_url: str):
        """
        Function to extract all ads from a given page from OtoDom webservice
        Args:
            page_url (str): link to the OtoDom page
        
        Returns:
            soup (bs4.BeautifulSoup): bs4.BeautifulSoup object for future downloading data

        """

        # parser data from created link
        page = requests.get(page_url)
        print(page)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        return soup

    def create_list_of_ulrs(self, soup) -> list:
        """
        Function to extract ftom Oto Dom page links to download data from particular ads
        
        Args:
            soup (bs4.BeautifulSoup): bs4.BeautifulSoup object
        
        Returns:
            list: List of linkt to the ads from given page

        """
        
        # find all urls to the ads on the selected page - create lists of them
        list_of_url = []
        for a in soup.find_all('a', {"class": "css-lsw81o e1dfeild2"}, href=True):
            one_url = a['href']
            list_of_url.append(one_url)
            
        return list_of_url

    def extract_olx_data(self, list_of_url: list) -> pd.DataFrame:
        """
        Function to extrat ads details about homes & flat in otodom website
        
        Args:
            list_of_url (list): List of urls to extract data
        
        Returns:
            pdDataFrame: Data Frame with details about ads from given links

        """
        
        full_df_ads_details = []

        for index, one_url in enumerate(list_of_url):

            one_add_page = []
            page_one_add = []
            soup_one_add = []
            json_data = []
            add_details_df = pd.DataFrame()

            one_add_page = f'https://www.otodom.pl{one_url}'

            page_one_add = requests.get(one_add_page)
            
            print(index, one_add_page, ':', page_one_add)
            
            soup_one_add = BeautifulSoup(page_one_add.content, 'html.parser')

            soup_one_add.find_all("div", {"class": "css-m97llu e16xl7020"})
            json_data = json.loads(soup_one_add.find('script', type='application/json').text)

            # extract fields from json in ads. Try except in selected field - if field doesn;t extis
            try:
                add_details_df["lang"] = pd.json_normalize(json_data['props']['pageProps'])['lang']
            except KeyError:
                add_details_df["lang"] = 'None'

            try:
                add_details_df["ad_id"] = pd.json_normalize(json_data['props']['pageProps'])['id']
            except KeyError:
                add_details_df["ad_id"] = 'None'

            try:
                add_details_df["url"] = pd.json_normalize(json_data['props']['pageProps'])['relativeUrl']
            except KeyError:
                add_details_df["url"] = 'None'

            try:
                add_details_df["ad_id2"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['id']
            except KeyError:
                add_details_df["ad_id2"] = 'None'

            try:
                add_details_df["market"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['market']
            except KeyError:
                add_details_df["market"] = 'None'

            try:
                add_details_df["publicId"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['publicId']
            except KeyError:
                add_details_df["publicId"] = 'None'

            try:
                add_details_df["slug"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['slug']
            except KeyError:
                add_details_df["slug"] = 'None'

            try:
                add_details_df["advertiserType"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['advertiserType']
            except KeyError:
                add_details_df["advertiserType"] = 'None'

            try:
                add_details_df["createdAt"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['createdAt']
            except KeyError:
                add_details_df["createdAt"] = 'None'

            try:
                add_details_df["modifiedAt"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['modifiedAt']
            except KeyError:
                add_details_df["modifiedAt"] = 'None'

            try:
                add_details_df["description"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['description']
            except KeyError:
                add_details_df["description"] = 'None'

            try:
                add_details_df["title"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['title']
            except KeyError:
                add_details_df["title"] = 'None'

            try:
                add_details_df["full_url"] = pd.json_normalize(json_data['props']['pageProps']['ad'])['url']
            except KeyError:
                add_details_df["full_url"] = 'None'

            try:
                add_details_df["price"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("key == 'price'").reset_index()['value']
            except KeyError:
                add_details_df["price"] = 'None'

            try:
                add_details_df["m"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("key == 'm'").reset_index()['value']
            except KeyError:
                add_details_df["m"] = 'None'

            try:
                add_details_df["price_per_m"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("key == 'price_per_m'").reset_index()['value']
            except KeyError:
                add_details_df["price_per_m"] = 'None'

            try:
                add_details_df["rooms_num"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("key == 'rooms_num'").reset_index()['value']
            except KeyError:
                add_details_df["rooms_num"] = 'None'

            try:
                add_details_df["floor_no"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("label == 'Piętro'").reset_index()['localizedValue']
            except KeyError:
                add_details_df["floor_no"] = 'None'

            try:
                add_details_df["heating"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("key == 'heating'").reset_index()['value']
            except KeyError:
                add_details_df["heating"] = 'None'

            try:
                add_details_df["building_ownership"] = pd.json_normalize(json_data['props']['pageProps']['ad']['characteristics']).query("key == 'building_ownership'").reset_index()['value']
            except KeyError:
                add_details_df["building_ownership"] = 'None'

            try:
                add_details_df["city"] = pd.json_normalize(json_data['props']['pageProps']['ad']['target'])['City']
            except KeyError:
                add_details_df["city"] = 'None'

            try:
                add_details_df["City_id"] = pd.json_normalize(json_data['props']['pageProps']['ad']['target'])['City_id']
            except KeyError:
                add_details_df["City_id"] = 'None'

            try:
                add_details_df["Country"] = pd.json_normalize(json_data['props']['pageProps']['ad']['target'])['Country']
            except KeyError:
                add_details_df["Country"] = 'None'

            try:
                add_details_df["MarketType"] = pd.json_normalize(json_data['props']['pageProps']['ad']['target'])['MarketType']
            except KeyError:
                add_details_df["MarketType"] = 'None'

            try:
                add_details_df["PriceRange"] = pd.json_normalize(json_data['props']['pageProps']['ad']['target'])['PriceRange']
            except KeyError:
                add_details_df["PriceRange"] = 'None'

            try:
                add_details_df["latitude"] = pd.json_normalize(json_data['props']['pageProps']['ad']['location']['coordinates'])['latitude']
            except KeyError:
                add_details_df["latitude"] = 'None'

            try:
                add_details_df["longitude"] = pd.json_normalize(json_data['props']['pageProps']['ad']['location']['coordinates'])['longitude']
            except KeyError:
                add_details_df["longitude"] = 'None'

            try:
                add_details_df["district_name"] = pd.json_normalize(json_data['props']['pageProps']['ad']['location']['address'])['district.code']
            except KeyError:
                add_details_df["district_name"] = 'None'

            try:
                add_details_df["district.id"] = pd.json_normalize(json_data['props']['pageProps']['ad']['location']['address'])['district.id']
            except KeyError:
                add_details_df["district.id"] = 'None'

            full_df_ads_details.append(add_details_df)
            time.sleep(self.sys_sleeping)
                
        full_df_ads_details = pd.concat(full_df_ads_details, axis=0)    
        return full_df_ads_details
        

    def download_data(self):      
        """
        function for downloading data from Oto Dom Service

        Returns:
            pd.DataFrame: Data Frame with data about ads from Oto Dom service
        """
        
        full_df_ads_data_details = []
        full_ds = []
        date_of_download = date.today()
        limit_ads_one_page = int(self.limit)

        running = True
        page_counter = 1

        # while loop for downloading more than one page on oto dom
        while running:

            next_link_to_download = []
            next_soup_page = []
            next_list_of_ads_links = []
            next_ads_details = []

            #  step 1 - create a main link for downloading data
            next_link_to_download = scrape_otodom_data.create_link_page_to_download(self, page_counter = page_counter)

            # step 2 - scrap page for downloading data

            next_soup_page = scrape_otodom_data.define_page_to_extract(self, page_url = next_link_to_download)

            # step 3 - find all links (ads) on the scrapped pag

            next_list_of_ads_links = scrape_otodom_data.create_list_of_ulrs(self, soup = next_soup_page)

            print(next_link_to_download, '/ads to download: ', len(next_list_of_ads_links))
            ads_to_download_in_page = len(next_list_of_ads_links)

            # step 4 - extract all details from found ads on the page
            try:
                next_ads_details = scrape_otodom_data.extract_olx_data(self, list_of_url = next_list_of_ads_links)
                next_ads_details.to_csv(f'{self.path_to_save_batch_files}/data_part_{page_counter}_{date_of_download}.csv')
            except ValueError:
                running = False
                print('No More Data = stop downloading data')

            full_df_ads_data_details.append(next_ads_details)

            page_counter += 1

            if ads_to_download_in_page < limit_ads_one_page:
                print('No More Data = stop downloading data')
                break

        # full_df_ads_data_details = full_df_ads_data_details[ : -1]
        full_ds = pd.concat(full_df_ads_data_details, axis=0)

        full_ds.to_csv(f'{self.path_to_save_full_files}/full_oto_dom_data_{date_of_download}.csv')
        
        return full_ds

