from bs4 import BeautifulSoup
import requests
import time
import time
from typing import Union
from src.OtoData_extract import *
from src.OtoData_buildURL import *

def create_ad_page_to_extract(one_url: str) -> str:

    """
    Function for prepare an url for data extract
    
    Args:
        one_url (str): bs4.BeautifulSoup object
    
    Returns:
        str: url ready for scraping data

    """

    one_add_page = f'https://www.otodom.pl{one_url}'
    return one_add_page


def create_list_of_ulrs(soup, scrape_params: dict) -> list:
    
    """
    Function to extract ftom Oto Dom page links to download data from particular ads
    
    Args:
        soup (bs4.BeautifulSoup): bs4.BeautifulSoup object
    
    Returns:
        list: List of linkt to the ads from given page

    """
    
    # find all urls to the ads on the selected page - create lists of them
    list_of_url = []
    for a in soup.find_all('a', {"class": scrape_params['urls_class'][0]}, href=True):
        one_url = a['href']
        list_of_url.append(one_url)
        
    return list_of_url

def extract_html_page(page_url: str):
   
    """
    Function to extract all ads from a given page from OtoDom webservice
    Args:
        page_url (str): link to the OtoDom page
    
    Returns:
        soup (bs4.BeautifulSoup): bs4.BeautifulSoup object for future downloading data

    """
    # parser data from created link
    page = requests.get(page_url)
    # if status is 404 it means that ads params probably are wrong 
    # remember collecting data up to the city level with county law
    if page.status_code == 404:
        print(page)
        raise ValueError("Page dosn't exist. Check params!")
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def download_data(
        query_params: dict, 
        scrape_params: dict, 
        page_counter: int
) -> Union[list, int]:
    
    """
    Function for downloading data from Oto Dom service
    
    Args:
        query_params (dict):dictionary with params for looking for oto dom ads for scraping
        scraper_config (dict): dictionary with specific scrape params from a oto dom page
        page_counter (int): value of the next page 
    
    Returns:
        list: bs4.BeautifulSoup object for future downloading data
        int: number of urls for download data 
            - checking if list of urls is shorter than minimum ads on page

    """
    # 1st step - create a main page for download  - params of looked apartaments given in config file
    main_page_url = create_link_page_to_download(query_params, page_counter)
    # 2nd step - extrat page for scraping using beautiful soup package
    page_html = extract_html_page(main_page_url)
    # 3rd step - create list of url of ads for scraping
    urls = create_list_of_ulrs(page_html, scrape_params)
    # 3a - check how many ads is for scraping. If number of ads is less than minimum defined value in one page
    # scraper should download only one page of ads
    n_urls = len(urls)

    print(f'n_ads: {n_urls} ,: {main_page_url}')
    
    full_ads_data = []

    for i in urls:
        #prepare url of on ad for extracting data
        one_ad_page = create_ad_page_to_extract(i) 
        print(one_ad_page)
        # using bs package - extract page
        one_ad_hmlt_extract = extract_html_page(one_ad_page) 
        # extract ads details from json in page
        json_ad = extract_ad_json(
            add_soup = one_ad_hmlt_extract, 
            scraper_config = scrape_params
        )
        # extract ad details defined in scraper config
        one_add_data = full_ad_details(
            json_data = json_ad, 
            scraper_config = scrape_params
        )
        full_ads_data.append(one_add_data)
        time.sleep(query_params['sys_sleep'])

    return full_ads_data, n_urls
    
    
