from datetime import datetime
from typing import Dict, List
from lib import warframe_status
import re

from lib.common import format_timedelta, format_unique_name
from services.world import vendor
def _clean_name(name:str)-> str:
    return re.sub(r'\b(M P V |Dual Pack|Single Pack|Set|Prime)\b', '', name).strip()

def info():
    response = warframe_status.world("vaultTrader")
    if response:
        return vendor.get_inventory(response,"regal_aya","aya")
    else: return {}

def pack():
    response = warframe_status.world("vaultTrader")
    if response:
        inventory:List[Dict] = response.get("inventory",[])
        packs:List[Dict] = []
        if len (inventory) > 0:
            for index ,item in enumerate(inventory):
                if "MegaPrimeVault" in item.get("uniqueName","") and "Pack" in item.get("item",""):
                    items = _clean_name(item.get("item","")).split(" ")
                    include = []
                    if len(items)>0:
                        for name in items:
                            item_search = warframe_status.items(warframe_status.WarframeStatusSearchParams(name,"name",type="warframes",only=["imageName","name","uniqueName"]))
                            include.append(item_search[0] if len(item_search)>0 else {} )
                    packs.append({
                        "uniqueName": item.get("uniqueName", "Unknown"),
                        "price": item.get("ducats", 0),
                        "currency": "regal_aya",
                        "include": include
                    })

        time = datetime.strptime(response.get("expiry",""),"%Y-%m-%dT%H:%M:%S.%fZ")
        
        return {
            "expire": time,
            "time": format_timedelta(time-datetime.today(),day=True),
            "packs":packs
        }
    else: return {}