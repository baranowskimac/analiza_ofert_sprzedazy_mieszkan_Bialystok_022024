from dataclasses import dataclass
from typing import List
import yaml


CONFIG_PATH = "./config/parser.yaml"


@dataclass
class ParserConfig:
    olx_a_class: str
    url_root: str
    url_core: str
    url_query_suffix: str
    extract_attributes: dict
    characteristics: List[str]


def get_parser_config() -> ParserConfig:
    with open(CONFIG_PATH, "r") as file:
        yaml_content = file.read()
        return ParserConfig(**yaml.safe_load(yaml_content))
