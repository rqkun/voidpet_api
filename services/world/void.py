from lib import warframe_status

from services.world import vendor
def info():
    response = warframe_status.world("voidTrader")
    if response:
        return vendor.get_inventory(response,"ducats","credits")
    else: return {}