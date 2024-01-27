def regional_params(query_params: dict, x = 'country'):
    return {
        'country': "cala-polska?",
        'region': f"{query_params['region']}?",
        'city': f"{query_params['region']}/{query_params['city']}/{query_params['city']}/{query_params['city']}?distanceRadius={query_params['distance_radius']}?"
    }.get(x) 

def build_regional_url(query_params: dict):
    if (query_params['region'] is None) & (query_params['city'] is None):
        return regional_params(x = 'country', query_params = query_params)
    elif (query_params['region'] is not None) & (query_params['city'] is None):
        return regional_params(x = 'region', query_params = query_params)
    elif (query_params['region'] is not None) & (query_params['city'] is not None):
        return regional_params(x = 'city', query_params = query_params)
    elif (query_params['region'] is None) & (query_params['city'] is not None):
        raise ValueError("Check config. If city is chosen region must be choosen too!!!")

def create_link_page_to_download(query_params: dict, page_counter: int = 1):   
    """
    Function to extract all ads from a given page from OtoDom webservice
    Args:
    page_counter (int): value of the next page 
    Returns:
        page_url (str): url from Oto Dom service for downloading ads details
    """
    # create a link for downloading data
    url_suffix = f"&ownerTypeSingleSelect=ALL&priceMin={query_params['price_min']}&priceMax={query_params['price_max']}&by=DEFAULT&direction=DESC&viewType=listing&page={page_counter}"
    url_region = build_regional_url(query_params)
    page_url = f"{query_params['main_page']}/{query_params['offer_type']}/{query_params['apartament_type']}/{url_region}limit={query_params['limit']}{url_suffix}"

    return page_url

