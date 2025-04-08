
from datetime import datetime
from typing import Dict, List, Literal
from lib import warframe_status
import re

from lib.common import format_timedelta, format_unique_name
def _clean_name(name:str)-> str:
    return re.sub(r'\b(M P V |Dual Pack|Single Pack|Set|Prime)\b', '', name).strip()

def _batch_request(id_list:List,by:str,batch_size:int=10)->List[Dict]:
    result:List[Dict]=[]
    if len(id_list)>0:
        batch_size = 10
        for i in range(0, len(id_list), batch_size):
            current_batch = id_list[i:i+batch_size]
            batch_results = warframe_status.items(
                warframe_status.WarframeStatusSearchParams(
                    current_batch,
                    by,
                    type="items",
                    only=["imageName", "name", "uniqueName","wikiaThumbnail"]
                )
            )
            result.extend(batch_results)
    return result

def _non_unique_name_batch(items:List[Dict])->Dict:
    result:Dict={}
    if len(items) > 0:
        for item in items:
            found = warframe_status.items(
                    warframe_status.WarframeStatusSearchParams(
                        item["name"],
                        "name",
                        type="items",
                        only=["imageName", "name", "uniqueName", "wikiaThumbnail"]
                    ))
            result[item["uniqueName"]]= found[0] if len(found)>0 else {}
    return result

def get_inventory(data: dict, premium_curr: Literal["ducats","regal_aya"], free_curr: Literal["credits","aya"]) -> Dict:
    inventory:List[Dict] = data.get("inventory",[])
    unique_name_list:List[str] = []
    normal_items:List[Dict] = []
    extractors:List[Dict] =[]
    merged_list:List[Dict] = []

    if len(inventory) > 0:
        for item in inventory:

            item["price"] = {
                "premium": {
                    "amount": 0,
                    "image": ""
                },
                "free": {
                    "amount": 0,
                    "image": ""
                },
            }
            if item["ducats"] is not None:
                item["price"]["premium"]["amount"] = item["ducats"]
                item["price"]["premium"]["image"] = f"https://wiki.warframe.com/images/{premium_curr}.png"
            if item["credits"]:
                item["price"]["free"]["amount"] = item["credits"]
                item["price"]["free"]["image"] = f"https://wiki.warframe.com/images/{free_curr}.png"

            del item["ducats"]
            del item["credits"]

            if "MegaPrimeVault" in item.get("uniqueName","") and "Pack" in item.get("item",""):
                continue
            name = item.get("item","")
            if "Extractor" in name:
                extractors.append({
                    "uniqueName": item.get("uniqueName",""),
                    "name": _clean_name(name)+" Prime",
                    
                })
            else:
                unique_name_list.append(item.get("uniqueName",""))
    
        normal_items.extend(_batch_request(unique_name_list,"uniqueName",10))
        normal_items_dict = {item["uniqueName"]: item for item in normal_items}
        non_unique_item = _non_unique_name_batch(extractors)

        for item in inventory:
            if "MegaPrimeVault" in item.get("uniqueName","") and "Pack" in item.get("item",""):
                continue
            unique_name = item["uniqueName"]
            matching_key = None
            for dict_key in normal_items_dict:
                if format_unique_name(dict_key) in unique_name:
                    matching_key = dict_key
                    break
            if matching_key:
                merged_item = {**item, **normal_items_dict[matching_key]}
            elif unique_name in non_unique_item:
                merged_item = {**item, **non_unique_item[unique_name]}
            else:
                merged_item = item
                merged_item["name"] = item["item"]
                    
            if "name" in merged_item: del merged_item["item"]
            
            if "wikiaThumbnail" in merged_item and "Mods" in merged_item["uniqueName"]:
                merged_item["imageName"] = f"""{merged_item["wikiaThumbnail"]}"""
                
            elif "imageName" in merged_item: 
                merged_item["imageName"] = f"""https://cdn.warframestat.us/img/{merged_item["imageName"]}"""
            else: merged_item["imageName"] = "https://wiki.warframe.com/images/IconLotus.png"
            if "wikiaThumbnail" in merged_item: del merged_item["wikiaThumbnail"]
            merged_list.append(merged_item)

    end_time = datetime.strptime(data.get("expiry",""),"%Y-%m-%dT%H:%M:%S.%fZ")
    start_time =  datetime.strptime(data.get("activation",""),"%Y-%m-%dT%H:%M:%S.%fZ")
    return {
        "active": data.get("active",False),
        "start_time": start_time,
        "startString": format_timedelta(start_time-datetime.today(),day=True),
        "end_time": end_time,
        "endString": format_timedelta(end_time-datetime.today(),day=True),
        "inventory": merged_list
    }