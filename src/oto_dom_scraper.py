import json
from typing import List

import requests
import pandas as pd
from bs4 import BeautifulSoup

from config import get_parser_config


class OtodomDataScraper:
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
        page_limit: int = 25,
    ):
        self.page_limit = page_limit
        self.config = get_parser_config()

    def download_data(
        self,
        offer_type: str,
        apartment_type: str,
        region: str,
        price_min: int,
        price_max: int,
    ) -> pd.DataFrame:
        """Queries OLX page for matching offers, returns a df with params of matching offers."""
        matching_offers = self.query_all_pages(
            offer_type=offer_type,
            apartment_type=apartment_type,
            region=region,
            price_min=price_min,
            price_max=price_max,
        )
        offers_data = [self.parse_offer(url) for url in matching_offers]
        return pd.DataFrame(offers_data)

    def query_all_pages(
        self,
        offer_type: str,
        apartment_type: str,
        region: str,
        price_min: int,
        price_max: int,
    ) -> List[str]:
        """Return list of all urls for offers matching query"""

        page_number, all_urls = 0, []
        while True:
            page_number += 1
            page_urls = self.query(
                offer_type,
                apartment_type,
                region,
                price_min,
                price_max,
                page_number,
            )
            all_urls.extend(page_urls)
            if len(page_urls) < self.page_limit:
                break

        return all_urls

    def query(
        self,
        offer_type: str,
        apartment_type: str,
        region: str,
        price_min: int,
        price_max: int,
        page_number: int,
    ) -> List[str]:
        """Return list of urls for single page of offers matching query"""

        url = self.make_query_url(
            offer_type=offer_type,
            apartment_type=apartment_type,
            region=region,
            price_min=price_min,
            price_max=price_max,
            page_number=page_number,
            page_limit=self.page_limit,
        )
        soup = self._url_to_soup(url)

        page_urls = []
        for a in soup.find_all("a", {"class": self.config.olx_a_class}, href=True):
            page_urls.append(self.config.url_root + a["href"])

        return page_urls

    def make_query_url(
        self,
        offer_type: str,
        apartment_type: str,
        region: str,
        price_min: int,
        price_max: int,
        page_number: int,
        page_limit: int,
    ) -> str:
        url_core = self.config.url_core.format(
            offer_type=offer_type,
            apartment_type=apartment_type,
            region=region,
        )
        url_suffix = self.config.url_query_suffix.format(
            price_min=price_min,
            price_max=price_max,
            page_limit=page_limit,
            page_number=page_number,
        )
        return self.config.url_root + url_core + url_suffix

    def parse_offer(self, url) -> dict:
        """Extracts selected attributes from OLX offer under given url."""
        offer_json = self._offer_url_to_json(url)

        # extract raw attributes
        offer_parsed = {}
        for attr_name, attr_path in self.config.extract_attributes.items():
            attr_val = offer_json
            for attr_path_step in attr_path:
                attr_val = attr_val.get(attr_path_step, {})
            offer_parsed[attr_name] = attr_val or None

        # extract attributes from 'characteristics' map
        char_map = offer_json.get("ad", {}).get("characteristics", {})
        offer_characteristics = {
            c["key"]: c["value"]
            for c in char_map
            if c["key"] in self.config.characteristics
        }
        offer_parsed.update(offer_characteristics)

        return offer_parsed

    @staticmethod
    def _url_to_soup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    @staticmethod
    def _offer_url_to_json(url):
        soup = OtodomDataScraper._url_to_soup(url)
        json_page = json.loads(soup.find("script", type="application/json").text)
        return json_page["props"]["pageProps"]
