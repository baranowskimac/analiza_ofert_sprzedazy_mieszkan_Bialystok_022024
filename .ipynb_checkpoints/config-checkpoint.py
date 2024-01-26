from dataclasses import dataclass, asdict
from typing import List
import yaml


SCRAPER_PATH = "./config/scraper.yaml"
QUERY_PATH = "./config/query.yaml"


@dataclass
class ScraperConfig:
    a_class: str
    url_root: str
    url_core: str
    url_query_suffix: str
    extract_attributes: dict
    characteristics: List[str]


@dataclass
class QueryConfig:
    offer_type: str
    apartment_type: str
    region: str
    price_min: int
    price_max: int

    def to_dict(self):
        return asdict(self)


def get_scraper_config() -> ScraperConfig:
    with open(SCRAPER_PATH, "r") as file:
        yaml_content = file.read()
        return ScraperConfig(**yaml.safe_load(yaml_content))


def get_query_config() -> ScraperConfig:
    with open(QUERY_PATH, "r") as file:
        yaml_content = file.read()
        return QueryConfig(**yaml.safe_load(yaml_content))
