import json

def extract_ad_json(
        add_soup, 
        scraper_config: dict
) -> dict:
    
    """
    Function for extract a json with specific ad details

    Args:
        add_soup (soup): soup type object (from beuatiful soap) - scraped page
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict from json with specific ad details
    """

    add_soup.find_all("div", {"class": scraper_config['ad_css_class'][0]})
    json_data = json.loads(add_soup.find('script', type='application/json').text)
    return json_data['props']['pageProps']

def extract_ad_main_char(
        json_data: dict, 
        scraper_config: dict
) -> dict:
    
    """
    Function for extract from a json (dict) details about general attributes like:
    "lang", "id" "relativeUrl"

    Args:
        json_data (dict): dict from json with specific ad details
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict with specific ad details 
    """
    
    paresed_gen = {}
    for c in scraper_config['general_ad_attr']:
        ads_gen = {c: json_data.get(c, {})}
        paresed_gen.update(ads_gen)
    return paresed_gen

def extract_ad_details(
        json_data: dict, 
        scraper_config: dict
) -> dict:

    """
    Function for extract from a json (dict) details about ad attributes like:
    "id", "publicId", "market", "advertiserType", "title", "description", "url",
    "slug", "createdAt", "modifiedAt", "features"

    Args:
        json_data (dict): dict from json with specific ads details
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict with specific ad attributes 
    """

    parsed_details = {}
    add_details_json = json_data.get("ad", {})
    for c in scraper_config['ad_attr']:
        ad_details = {c: add_details_json.get(c, {})}
        parsed_details.update(ad_details)
    return parsed_details

def extract_target_details(
        json_data: dict, 
        scraper_config: dict
) -> dict:

    """
    Function for extract from a json (dict) details about ad target attributes like:
    "MarketType", "Area", "AreaRange", "Build_year", "Building_floors_num", "Country", 
    "City", "City_id", "Construction_status", "Extras_types", "Floor_no", "ProperType", 
    "Province", "Rooms_num", "Security_types", "Price", "PriceRange", "Price_per_m", "hidePrice"

    Args:
        json_data (dict): dict from json with specific ads details
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict with specific ad target attributes 
    """

    parsed_targets = {}
    add_target_json = json_data.get("ad", {}).get("target", {})
    for c in scraper_config['ad_targets_attr']:
        ad_targets = {c: add_target_json.get(c, {})}
        parsed_targets.update(ad_targets)
    return parsed_targets

def extract_ad_geo(
        json_data: dict, 
        scraper_config: dict
) -> dict:

    """
    Function for extract from a json (dict) details about ad geo attributes like:
    "latitude", "longitude"

    Args:
        json_data (dict): dict from json with specific ads details
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict with specific ad geo attributes 
    """

    parsed_geo = {}
    add_geo_json = json_data.get("ad", {}).get("location", {}).get('coordinates', {})
    for c in scraper_config['geo_attr']:
        ad_geo = {c: add_geo_json.get(c, {})}
        parsed_geo.update(ad_geo)
    return parsed_geo

def extract_ad_address(
        json_data: dict, 
        scraper_config: dict
) -> dict:

    """
    Function for extract from a json (dict) details about ad address attributes like:
    "street", "district", "city", "province"

    Args:
        json_data (dict): dict from json with specific ads details
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict with specific ad address attributes 
    """

    address_parsed = {}
    ad_address_json = json_data.get("ad", {}).get("location", {}).get('address', {})
    for c in scraper_config['address_attr']:        
        ad_address = {
            f'{c}_id': ad_address_json.get(c, {}).get('id', {}) if ad_address_json.get(c, {}) is not None else {},
            f'{c}_name': ad_address_json.get(c, {}).get('id', {}) if ad_address_json.get(c, {}) is not None else {},
        }
        address_parsed.update(ad_address)
    return address_parsed


def full_ad_details(
        json_data: dict, 
        scraper_config: dict
) -> dict:
        
    """
    Function for extract from a json (dict) details about all add attributes:

    Args:
        json_data (dict): dict from json with specific ads details
        scraper_config (dict): dictionary with specific scrape params from a oto dom page

    Returns:
        dict: dict with all ad attributes 
    """
    
    full_data = {}
    full_data.update(extract_ad_main_char(json_data, scraper_config))
    full_data.update(extract_ad_details(json_data, scraper_config))
    full_data.update(extract_target_details(json_data, scraper_config))
    full_data.update(extract_ad_geo(json_data, scraper_config))
    full_data.update(extract_ad_address(json_data, scraper_config))
    return full_data


