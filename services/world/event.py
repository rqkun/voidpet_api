from datetime import datetime
from typing import Dict, List
from lib import warframe_status
from lib.common import calculate_percentage_time, format_timedelta


def _clean(data)-> Dict:
    """Cleaning missing data from event API.

    Args:
        data (dict): json data of the event.

    Returns:
        dict: the cleaned data.
    """
    if 'currentScore' in data:
        pass
    else: 
        data['currentScore'] = 0
    
    if 'description' in data:
        pass
    else: 
        data['description'] = "No Description"
    
    if 'node' in data:
        pass
    else: 
        data['node'] = "No Data"
    return data


def rewards(data):
    """Get event rewards.

    Args:
        data (dict): event json data.

    Returns:
        list: list of reward names.
    """
    rewards = []
    if "interimSteps" in data and len(data["interimSteps"])>0:
        for step in data["interimSteps"]:
            if "reward" in step:
                if "items" in step["reward"] and len(step["reward"]["items"])>0:
                    for item in step["reward"]["items"]:
                        rewards.append(item)

    if "rewards" in data and len(data["rewards"])>0:
        for reward in data["rewards"]:
            if "items" in reward and len(reward["items"])>0:
                for item in reward["items"]:
                    rewards.append(item)

    return rewards


def info():
    result = []
    response = warframe_status.world("events")
    if len(response) >0:
        sorted_event:List[Dict] = sorted(
        [_clean(event) for event in response],
        key=lambda x: x["expiry"]
        )


        for event in sorted_event:
            percentage = calculate_percentage_time(event["activation"],event["expiry"])
            if percentage < 1:
                node = event["victimNode"] if "victimNode" in event else event["node"]
                time = datetime.strptime(event["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")
                result.append({
                            "percentage": percentage if percentage <= 1 else 1,
                            "expire": time,
                            "time": format_timedelta(time-datetime.today(),day=True),
                            "mission":{
                                "node": node,
                                "description": event.get("description","").replace("Operation: ", ""),
                                },
                            "rewards": rewards(event),
                        })
    return {
        "result": result,
        "completed": len(response)- len(result)
    }