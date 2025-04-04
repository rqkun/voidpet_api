from enum import Enum
from typing import Literal
from lib import warframe_export
from lib.classes.export import AppExports
    
def find(search_key:str, attribute:Literal["uniqueName","name"]="name",
         file=Literal["DRONES",
                    "COSMETICS",
                    "FLAVOURS",
                    "BUNDLES",
                    "GEARS",
                    "KEYS",
                    "MANIFEST",
                    "RECIPES",
                    "REGIONS",
                    "RELIC_ARCANE",
                    "RESOURCES",
                    "SENTINELS",
                    "SORTIES",
                    "NIGHTWAVE" ,
                    "RAILJACK",
                    "INTRINSICS",
                    "OTHER",
                    "UPGRADES",
                    "MOD_SET",
                    "AVIONICS",
                    "FOCUS_UPGRADES",
                    "WARFRAMES",
                    "ABILITIES",
                    "WEAPONS",
                    "RAILJACK_WEAPONS"])->dict[str,]:
    
    export_enum:Enum = getattr(AppExports, file)  # Get the enum member dynamically
    export_file = warframe_export.export_open(export_enum.value)
    for item in export_file:
        if item.get(attribute, None):
            if search_key in item[attribute]:
                return item
    return None