from datetime import datetime
from typing import Dict, List
from lib import warframe_status
from lib.common import calculate_percentage_time, format_timedelta

def info():
    result:List[Dict] = []
    response = warframe_status.world("invasions")
    
    if response:
        for invasion in response:
            if not invasion.get("completed",True):
                attacker = invasion.get("attacker", None)
                
                if attacker:
                    atk_faction = attacker.get("faction","")
                    atk_rewards = attacker.get("reward", None)
                    if atk_rewards:
                        atk_reward = {"name":atk_rewards.get("asString","None"),
                                      "imageName":atk_rewards.get("thumbnail","None")}
                    else: atk_reward = None
                    
                defender = invasion.get("defender", None)
                if defender:
                    def_faction = defender.get("faction","")
                    def_rewards = defender.get("reward", "None")
                    if def_rewards:
                        def_reward = {"name":def_rewards.get("asString","None"),
                                      "imageName":def_rewards.get("thumbnail","None")}
                    else: def_reward = None

                node = invasion.get("node","")
                completion = invasion.get("completion",0)
                atk_completion = 100 - int(completion)
                
                
                result.append({
                    "node":node,
                    "requiredRuns": invasion.get("requiredRuns",30000) + invasion.get("count",0),
                    "attack":{
                        "score": atk_completion,
                        "faction": atk_faction,
                        "rewards": atk_reward
                    },
                    "defend":{
                        "score": int(completion),
                        "faction": def_faction,
                        "rewards": def_reward
                    }
                })
    return {
        "result":result,
        "completed": len(response) - len(result)
        }