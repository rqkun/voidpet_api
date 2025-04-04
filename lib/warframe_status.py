import logging
from typing import Dict, List, Literal, Union
import requests
from lib.common import format_unique_name, raise_detailed_error
from lib.common import encode_identifier

class WarframeStatusSearchParams:
    def __init__(self, identifier:Union[List[str],str], by, type:str=Literal["items","weapons","warframes"],only=None, remove=None):
        self.identifier = encode_identifier(self._map_identifier(identifier,by))
        self.by = by
        self.type = type
        self.only = only or []
        self.remove = remove or []

    def _map_identifier(self,identifier, by):
        if isinstance(identifier, list):
            list_str=[]
            if by =="uniqueName":
                for id in identifier:
                    list_str.append(format_unique_name(id))
            return ",".join(list_str)
        else: 
            return format_unique_name(identifier) if by =="uniqueName" else identifier

    def to_query_string(self):
        filters = []
        if self.by:
            filters.append(f"by={self.by}")
        if self.only:
            only_query = ",".join(self.only)
            filters.append(f"only={only_query}")
        if self.remove:
            remove_query = ",".join(self.remove)
            filters.append(f"remove={remove_query}")
        return "&".join(filters)


def world(path=None) -> Union[List[Dict],Dict]:
    """API request to get current world state data.
    Args:
        path(str):
            "events": "Current events",\n
            "alerts": "Active alerts",\n
            "news": "Active news",\n
            "voidTrader": "Baro Ki'Teer's inventory",\n
            "vaultTrader": "Varzia's prime vault",\n
            "invasions": "Ongoing invasions",\n
            "sortie": "Daily sortie mission",\n
            "cetusCycle": "Cetus day/night cycle",\n
            "vallisCycle": "Orb Vallis warm/cold cycle",\n
            "cambionCycle": "Cambion Drift Fass/Vome cycle",\n
            "zarimanCycle": "Zariman Grineer/Corpus cycle",\n
            "duviriCycle": "Duviri Joy/Anger/Envy/Sorrow/Fear cycle"\n
    Returns:
        dict: World state data
    """
    base_url = "https://api.warframestat.us"
    route = f"/{path}" if path is not None else ""
    request_url = f"{base_url}/pc{route}?language=en"
    headers = {"accept": "application/json"}
    response = requests.get(request_url,headers=headers)
    raise_detailed_error(response)
    return response.json()


def items(params:WarframeStatusSearchParams)-> Union[List[Dict], Dict]:
    """API request to get item searchable data.

    Args:
        params (WarframeStatusSearchParams): The search parameters.

    Returns:
        list: List of items if found, otherwise empty.
    """
    base_url = "https://api.warframestat.us"
    query_string = params.to_query_string()
    request_url = f"{base_url}/{params.type}/search/{params.identifier}?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    return response.json()

def item(params:WarframeStatusSearchParams) -> dict:
    """API request to get item searchable data.

    Args:
        params (WarframeStatusSearchParams): The search parameters.

    Returns:
        list: List of items if found, otherwise empty.
    """
    base_url = "https://api.warframestat.us"
    query_string = params.to_query_string()
    request_url = f"{base_url}/{params.type}/{params.identifier}?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    if response.status_code == 404:
        return {}
    elif response.status_code == 200:
        return response.json()
    else:
        raise_detailed_error(response)
