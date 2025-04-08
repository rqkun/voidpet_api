from typing import Union
import requests
from lib.common import raise_detailed_error

class RivenSearchParams:
    def __init__(self, weapon_url_name, buyout_policy=None, positive_stats=None,
                 negative_stats=None, operation=None, re_rolls_min=None,
                 re_rolls_max=None, polarity=None,sort="price_asc"):
        self.identifier = weapon_url_name
        self.buyout_policy = buyout_policy
        self.positive_stats = positive_stats or []
        self.negative_stats = negative_stats or []
        self.operation = operation
        self.re_rolls_min = re_rolls_min
        self.type = "riven"
        self.re_rolls_max = re_rolls_max
        self.polarity = polarity
        self.sort = sort

    def to_query_string(self):
        filters = []
        filters.append(f"type={self.type}")
        if self.identifier:
            filters.append(f"weapon_url_name={self.identifier}")
        if self.buyout_policy:
            filters.append(f"buyout_policy={self.buyout_policy}")
        if self.positive_stats:
            positive_query = ",".join(self.positive_stats)
            filters.append(f"positive_stats={positive_query}")
        if self.negative_stats:
            negative_query = ",".join(self.negative_stats)
            filters.append(f"negative_stats={negative_query}")
        if self.operation:
            filters.append(f"operation={self.operation}")
        if self.re_rolls_min is not None:
            filters.append(f"re_rolls_min={self.re_rolls_min}")
        if self.re_rolls_max is not None:
            filters.append(f"re_rolls_max={self.re_rolls_max}")
        if self.polarity:
            filters.append(f"polarity={self.polarity}")
        if self.sort:
            filters.append(f"sort_by={self.sort}")
        return "&".join(filters)

def items(url_path=None,order=False,include=False)-> Union[dict,None]:
    """API request to get item's orders.

    Args:
        url_path (str): warframe.market Item path.

    Returns:
        dict: Orders data
    """
    if url_path is not None:
        if order:
            order_req = "/orders" 
            if include: 
                order_req = f"{order_req}?include=item"
        else: order_req = ""
        path = f"/{url_path}{order_req}"
    else:
        path =""
    base_url = "https://api.warframe.market/v1"
    
    request_url = f"{base_url}/items{path}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    if response.status_code == 404:
        return None
    elif response.status_code == 200:
        list_included:list = []
        img_link = ""
        if "include" in response.json():
            if "item" in response.json()["include"]:
                list_included:list = response.json()["include"]["item"].get("items_in_set",[])
                for item in list_included:
                    if item.get("set_root",False):
                        img_link = item["en"].get("icon","")
                        break
        return{
                "url": url_path,
                "img_link": img_link,
                "orders": response.json()["payload"]["orders"]
            }
    raise_detailed_error(response)
    return response.json()


def rivens_info(key:str):
    """API request to get riven items data.

    Returns:
        dict: All riven items data
    """
    if key not in ["items","attributes"]:
        raise ValueError("Riven API - Implemented key. (items, attributes)")
    base_url = "https://api.warframe.market/v1"
    request_url = f"{base_url}/riven/{key}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    raise_detailed_error(response)
    data = response.json()
    obj = data.get("payload", {}).get(key, [])
    return obj if obj else None


def rivens_auction(params:RivenSearchParams):
    """
    API request to get riven attribute data.

    Args:
        params (RivenSearchParams): The search parameters.

    Returns:
        list or None: List of auctions if found, otherwise None.
    """
    base_url = "https://api.warframe.market/v1"
    query_string = params.to_query_string()
    request_url = f"{base_url}/auctions/search?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    data = response.json()
    obj = data.get("payload", {}).get("auctions", [])
    return obj if obj else None
