from datetime import datetime, timezone
import logging
from statistics import median
from typing import Literal
from numpy import average
import pandas as pd

import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))

parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))

sys.path.insert(0, parent_dir_path)

from lib import google_api, warframe_market, warframe_status



def process_item_data(items:list)->list:
    """Process a list of items into a DataFrame-ready format."""
    def sort_open_close(data):
        
        # Ensure status is a list of valid statuses
        df = pd.DataFrame(data)

        # Convert last_seen to datetime
        # df["last_seen"] = pd.to_datetime(df["user"].apply(lambda x: x["last_seen"]),format="%Y-%m-%dT%H:%M:%S.%f%z")
        df["creation_date"] = pd.to_datetime(df["creation_date"],format="%Y-%m-%dT%H:%M:%S.%f%z")
        df["last_update"] = pd.to_datetime(df["last_update"],format="%Y-%m-%dT%H:%M:%S.%f%z")
        
        # Get today's date in UTC
        today = datetime.now(timezone.utc).date()

        # Filter only today's data & status = ingame
        filtered_df = df[((df["creation_date"].dt.date == today) | (df["last_update"].dt.date == today)) & (df["visible"]==True) & (df["order_type"]=="sell")]

        # Sort by last_seen (earliest to latest)
        sorted_df = filtered_df.sort_values(by=["last_update","platinum"], ascending=[True,False])
        
        open = sorted_df.iloc[0]["platinum"] if not sorted_df.empty else None
        # Get last element
        close = sorted_df.iloc[-1]["platinum"] if not sorted_df.empty else None
        
        prices_df = filtered_df.sort_values(by="platinum", ascending=True)

        minp = prices_df.iloc[0]["platinum"]
        maxp = prices_df.iloc[-1]["platinum"]
        
        median_ = median(prices_df["platinum"])
        avg = average(prices_df["platinum"])
        
        return open, close, minp, maxp, median_, avg
        # Status priority for sorting (lower value means higher priority)

    def calculate_price_stats(orders):
        """Calculate min, median, and max prices from a list of orders."""
        if not orders:
            return 0, 0, 0, 0, 0, 0
        return sort_open_close(orders)
    
    processed_data = []

    for item in items:
        open_price,close_price,min_plat, max_plat, median_plat, avg_plat = calculate_price_stats(item["orders"])
        processed_data.append({
            "Image": f"""https://warframe.market/static/assets/{item["img_link"]}""",
            "Name": item["url"].replace("_", " ").replace(" set", "").title(),
            "Count": len(item["orders"]),
            "Average": int(avg_plat),
            "Median": int(median_plat),
            "Min": int(min_plat),
            "Max": int(max_plat),
            "Open": int(open_price),
            "Close": int(close_price),
        })

    return processed_data

def get_primes():
    sens =[]
    
    p_frame = warframe_status.items(warframe_status.WarframeStatusSearchParams("prime","name",type="warframes",only=["name","category"]))
    frames = [item["name"] for item in p_frame]
    
    p_weap = warframe_status.items(warframe_status.WarframeStatusSearchParams("prime","name",type="weapons",only=["name","category"]))
    weaps = [item["name"] for item in p_weap]
    
    
    p_items = warframe_status.items(warframe_status.WarframeStatusSearchParams("prime","name",type="items",only=["name","category"]))
    
    for item in p_items:
        if item["category"] != "Sentinels":
            continue
        sens.append(item["name"])
    
    return frames,weaps,sens

# def insert(df: pd.DataFrame, sheet: pd.DataFrame):
#     """Insert or update data in the sheet, ensuring timestamps are in GMT."""
#     def convert_index(name: str):
#         """Generate an index using Name and current GMT date."""
#         name = f"""{name.replace(" ", "-")}-{datetime.now(timezone.utc).strftime("%d-%m-%Y-UTC")}"""
#         return name
    
#     if len(sheet) ==0 or list(sheet.columns) != ["Id", "Name", "Count", "Median", "Average", "Min", "Max", "Open", "Close", "Changed"]:
#         sheet= pd.DataFrame(columns=["Id", "Name", "Count", "Median", "Average", "Min", "Max", "Open", "Close", "Changed"])
#     sheet.set_index("Id", inplace=True)

#     current_time = datetime.now(timezone.utc).strftime("%d/%m/%Y - %H:%M:%S UTC")
#     for _, item in df.iterrows():
#         index_name = convert_index(item["Name"])

#         sheet.loc[index_name] = [
#             item["Name"],
#             int(item["Count"]),
#             int(item["Average"]),
#             int(item["Median"]),
#             int(item["Min"]),
#             int(item["Max"]),
#             sheet.at[index_name, "Open"] if index_name in sheet.index else int(item["Open"]),
#             int(item["Close"]),
#             current_time
#         ]

#     return sheet
def insert(df: pd.DataFrame, sheet: pd.DataFrame):
    """Insert or update data in the sheet, ensuring timestamps are in GMT."""
    def convert_index(name: str):
        """Generate an ID using Name and current GMT date."""
        name = f"""{name.replace(" ", "-")}-{datetime.now(timezone.utc).strftime("%d-%m-%Y-UTC")}"""
        return name
    
    # Check if sheet is empty or doesn't have the expected columns
    if len(sheet) == 0 or list(sheet.columns) != ["Id", "Name", "Count", "Median", "Average", "Min", "Max", "Open", "Close", "Changed"]:
        sheet = pd.DataFrame(columns=["Id", "Name", "Count", "Median", "Average", "Min", "Max", "Open", "Close", "Changed"])
    
    # Create a working copy - no need to set the index now
    working_sheet = sheet.copy()
    
    current_time = datetime.now(timezone.utc).strftime("%d/%m/%Y - %H:%M:%S UTC")
    
    for _, item in df.iterrows():
        id_value = convert_index(item["Name"])
        
        # Check if this ID already exists in the sheet
        existing_row = working_sheet[working_sheet['Id'] == id_value]
        
        new_row = {
            "Id": id_value,
            "Name": item["Name"],
            "Count": int(item["Count"]),
            "Median": int(item["Median"]),
            "Average": int(item["Average"]),
            "Min": int(item["Min"]),
            "Max": int(item["Max"]),
            "Close": int(item["Close"]),
            "Changed": current_time
        }
        
        # Handle the Open value
        if len(existing_row) > 0:
            new_row["Open"] = existing_row["Open"].values[0]  # Use existing Open value
        else:
            new_row["Open"] = int(item["Open"])  # Use new Open value
        
        # If ID exists, update the row
        if len(existing_row) > 0:
            idx = existing_row.index[0]
            for col, val in new_row.items():
                working_sheet.at[idx, col] = val
        else:
            # Otherwise append a new row
            working_sheet = pd.concat([working_sheet, pd.DataFrame([new_row])], ignore_index=True)
    
    return working_sheet

def get_orders(item_names:list, df_type=Literal["prime_frames","prime_weapons","prime_sentinels"]):
    
    def process_history(_gsread_client:google_api.GoogleSheetConnection,sheet_name:str)-> pd.DataFrame:
        worksheet = pd.DataFrame(_gsread_client.open(sheet_name,f"{datetime.today().year}"))
        return worksheet
    
    client = google_api.get_instance()

    to_year = datetime.today().year
    
    logging.warning(f"Item request {df_type}")
    orders =[]
    ids = [f"{item} set".lower().replace(" ","_") for item in item_names]
    for id in ids:
        order_list = warframe_market.items(id,True,True)
        if order_list is None:
            continue
        orders.append(order_list)
    logging.warning(f"Process {df_type}")
    orders_df = pd.DataFrame(process_item_data(orders))
    logging.warning(f"Pulling history of {df_type}")
    history_df = process_history(client,df_type)
    whole_df = insert(df=orders_df,sheet=history_df)

    logging.warning(f"Update Sheet {df_type}")
    client.update(spreadsheet=df_type,dataframe=whole_df,worksheet=f"{to_year}")
    logging.warning(f"Finish {df_type}")

    
if __name__ == "__main__":
    
    frames,weaps,sens = get_primes()
    get_orders(frames,"prime_frames")
    get_orders(weaps,"prime_weapons")
    get_orders(sens,"prime_sentinels")