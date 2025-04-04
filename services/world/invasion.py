from typing import Dict, List
from lib import warframe_status
from services import export
def _extract(data:dict, score):
    faction = data.get("faction","")
    rewards_dict = data.get("reward", None)
    rewards=[]
    if rewards_dict:
        items:List[Dict] = rewards_dict.get("countedItems",[])
        if len(items) >0:
            for item in items:

                item_search = warframe_status.item(warframe_status.WarframeStatusSearchParams(item.get("key","Unknown").replace(" Blueprint",""),"name",type="items",only=["imageName","name","uniqueName"]))

                if len(item_search) >0:
                    image = f"""https://cdn.warframestat.us/img/{item_search.get("imageName","")}""" 
                else:
                    image = f"""https://cdn.warframestat.us/img/{item.get("key","Unknown").split(" ")[-1].lower()}.png"""
                
                rewards.append({
                    "name":item.get("key","Unknown"),
                    "count":item.get("count",0),
                    "imageName": image
                }) 
                return {
            "score": score,
            "faction": faction,
            "rewards": rewards
            }

                
    return {
            "score": score,
            "faction": faction,
            "rewards": rewards
            }

def info():
    result:List[Dict] = []
    response = warframe_status.world("invasions")
    
    if response:
        for invasion in response:
            if not invasion.get("completed",True):
                attacker = invasion.get("attacker", None)
                defender = invasion.get("defender", None)
                node = invasion.get("node","Unknown")
                completion = int(invasion.get("completion",0))
                atk_completion = 100 - completion
                
                attacker_info = _extract(attacker,score = atk_completion) if attacker else None
                defender_info = _extract(defender,score = completion) if defender else None

                result.append({
                    "node": node,
                    "requiredRuns": invasion.get("requiredRuns",-1) + invasion.get("count",0),
                    "attack": attacker_info,
                    "defend": defender_info
                })
    return {
        "result": result,
        "completed": len(response) - len(result)
        }