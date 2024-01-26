from bs4 import BeautifulSoup
import requests
import time
import time
import yaml
from src.extract_ad_data import *

def read_config(config_path: str):
    with open(config_path, "r") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content

def create_link_page_to_download(
        main_page: str,
        offer_type: str,
        apartament_type: str,
        region: str,
        price_min: int,
        price_max: int,
        limit: int,
        page_counter: int = 1

):    
    """
    Function to extract all ads from a given page from OtoDom webservice
    Args:
    page_counter (int): value of the next page 
    Returns:
        page_url (str): url from Oto Dom service for downloading ads details
    """
    # create a link for downloading data
    url_suffix = f'&ownerTypeSingleSelect=ALL&priceMin={price_min}&priceMax={price_max}&by=DEFAULT&direction=DESC&viewType=listing&page={page_counter}'
    page_url = f'{main_page}/{offer_type}/{apartament_type}/{region}?limit={limit}{url_suffix}'
    return page_url


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
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

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

def create_ad_page_to_extract(one_url):
    one_add_page = f'https://www.otodom.pl{one_url}'
    return one_add_page


def download_data(query_params: dict, scrape_params: dict, page_counter = 1):

    main_page_url = create_link_page_to_download(
        main_page = query_params['main_page'],
        offer_type = query_params['offer_type'],
        apartament_type = query_params['apartament_type'],
        region = query_params['region'],
        price_min = query_params['price_min'],
        price_max = query_params['price_max'],
        limit = query_params['limit'],
        page_counter = page_counter
    )
    
    page_html = extract_html_page(main_page_url)
    urls = create_list_of_ulrs(page_html, scrape_params)
    n_urls = len(urls)

    print(f'n_ads: {n_urls} ,: {main_page_url}')
    
    full_ads_data = []

    for i in urls:
        one_ad_page = create_ad_page_to_extract(i)
        print(one_ad_page)
        one_ad_hmlt_extract = extract_html_page(one_ad_page)
        json_ad = extract_ad_json(add_soup = one_ad_hmlt_extract, scraper_config = scrape_params)
        one_add_data = full_ad_details(json_data = json_ad, scraper_config = scrape_params)
        full_ads_data.append(one_add_data)
        time.sleep(query_params['sys_sleep'])

    return full_ads_data, n_urls
    
    
