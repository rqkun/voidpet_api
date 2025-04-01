from typing import Literal
import requests
from lib.common import raise_detailed_error
from lib.common import encode_identifier

class WarframeStatusSearchParams:
    def __init__(self, identifier, by, type:str=Literal["items","weapons","warframes"],only=None, remove=None):
        self.identifier = identifier
        self.by = by
        self.type = type
        self.only = only or []
        self.remove = remove or []

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


def world(path=None):
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

def items(params:WarframeStatusSearchParams):
    """API request to get item searchable data.

    Args:
        params (WarframeStatusSearchParams): The search parameters.

    Returns:
        list: List of items if found, otherwise empty.
    """
    encoded_key = encode_identifier(params.identifier)
    base_url = "https://api.warframestat.us"
    query_string = params.to_query_string()
    request_url = f"{base_url}/{params.type}/search/{encoded_key}?{query_string}"
    headers = {"accept": "application/json"}
    response = requests.get(request_url, headers=headers)
    raise_detailed_error(response)
    return response.json()