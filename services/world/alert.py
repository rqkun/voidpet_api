from datetime import datetime
from typing import Dict, List
from lib import warframe_status
from lib.common import calculate_percentage_time, format_timedelta


def rewards(data):
    """Getting alert rewards with their images.

    Args:
        data (dict): alert data.

    Returns:
        list: list of alert rewards.
    """
    reward = []
    if 'mission' in data:
        if 'reward' in data['mission']:
                if 'items' in data['mission']['reward']:
                    if len(data['mission']['reward']['items']) > 0:
                        for item in data['mission']['reward']['items']:
                            reward.append({
                                            "item": item,
                                            "image": item,
                                            "amount": 1
                                        })
                if 'countedItems' in data['mission']['reward']:
                    if len(data['mission']['reward']['countedItems']) > 0:
                        for item in data['mission']['reward']['countedItems']:
                            reward.append({
                                            "item": item['key'],
                                            "image": item['key'],
                                            "amount": item['count']
                                        })
                if 'credits' in data['mission']['reward']:
                    if data['mission']['reward']['credits'] > 0:
                        reward.append({
                                        "item": "Credits",
                                        "image": "https://wiki.warframe.com/images/IconCredits.png",
                                        "amount": data['mission']['reward']['credits']
                                        })
    return reward


def info():
    result = []
    response = warframe_status.world("alerts")
    if len(response) >0:
        sorted_alert:List[Dict] = sorted(
        [item for item in response ],
        key=lambda x: x["expiry"]
        )
        for alert in sorted_alert:
            if alert.get("active",False):
                percentage = calculate_percentage_time(start=alert["activation"],end=alert["expiry"])
                if percentage < 1:
                    time = datetime.strptime(alert["expiry"],"%Y-%m-%dT%H:%M:%S.%fZ")
                    result.append({
                        "percentage": percentage if percentage <= 1 else 1,
                        "expire": time,
                        "time": format_timedelta(time-datetime.today(),day=True),
                        "mission":{
                            "type": alert.get("mission",{}).get("type"),
                            "node": alert.get("mission",{}).get("node"),
                            },
                        "rewards": rewards(alert),
                    })
    return {
        "result":result,
        "inactive": len(response)- len(result)
    }