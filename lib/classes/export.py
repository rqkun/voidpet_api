from enum import Enum


class AppExports(Enum):
    """The Web app pages locations. """
    DRONES = {
        "path": "ExportDrones_en.json",
        "object_name": "ExportDrones"
    }
    COSMETICS = {
        "path": "ExportCustoms_en.json",
        "object_name": "ExportCustoms"
    }
    FLAVOURS = {
        "path": "ExportFlavour_en.json",
        "object_name": "ExportFlavour"
    }
    BUNDLES = {
        "path": "ExportFusionBundles_en.json",
        "object_name": "ExportFusionBundles"
    }
    GEARS = {
        "path": "ExportGear_en.json",
        "object_name": "ExportGear"
    }
    KEYS = {
        "path": "ExportKeys_en.json",
        "object_name": "ExportKeys"
    }
    MANIFEST = {
        "path": "ExportManifest.json",
        "object_name": "Manifest"
    }
    RECIPES = {
        "path": "ExportRecipes_en.json",
        "object_name": "ExportRecipes"
    }
    REGIONS = {
        "path": "ExportRegions_en.json",
        "object_name": "ExportRegions"
    }
    RELIC_ARCANE = {
        "path": "ExportRelicArcane_en.json",
        "object_name": "ExportRelicArcane"
    }
    RESOURCES = {
        "path": "ExportResources_en.json",
        "object_name": "ExportResources"
    }
    SENTINELS = {
        "path": "ExportSentinels_en.json",
        "object_name": "ExportSentinels"
    }
    SORTIES = {
        "path": "ExportSortieRewards_en.json",
        "object_name": "ExportSortieRewards"
    }
    NIGHTWAVE = {
        "path": "ExportSortieRewards_en.json",
        "object_name": "ExportNightwave"
    }
    RAILJACK = {
        "path": "ExportSortieRewards_en.json",
        "object_name": "ExportRailjack"
    }
    INTRINSICS = {
        "path": "ExportSortieRewards_en.json",
        "object_name": "ExportIntrinsics"
    }
    OTHER = {
        "path": "ExportSortieRewards_en.json",
        "object_name": "ExportOther"
    }
    UPGRADES = {
        "path": "ExportUpgrades_en.json",
        "object_name": "ExportUpgrades"
    }
    MOD_SET = {
        "path": "ExportUpgrades_en.json",
        "object_name": "ExportModSet"
    }
    AVIONICS = {
        "path": "ExportUpgrades_en.json",
        "object_name": "ExportAvionics"
    }
    FOCUS_UPGRADES = {
        "path": "ExportUpgrades_en.json",
        "object_name": "ExportFocusUpgrades"
    }
    WARFRAMES = {
        "path": "ExportWarframes_en.json",
        "object_name": "ExportWarframes"
    }
    ABILITIES = {
        "path": "ExportWarframes_en.json",
        "object_name": "ExportAbilities"
    }
    WEAPONS = {
        "path": "ExportWeapons_en.json",
        "object_name": "ExportWeapons"
    }
    RAILJACK_WEAPONS = {
        "path": "ExportWeapons_en.json",
        "object_name": "ExportRailjackWeapons"
    }