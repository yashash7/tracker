from datetime import datetime
from typing import Dict, Any
from sqlalchemy import insert, select
from . import schemas
from .exceptions import Filter_Validation_Exception

# attributes
schema_type_assoc = {
    "alloc": schemas.Alloc,
    "burn": schemas.Burn,
    "fss_burn": schemas.FSS_Burn,
    "rotation_totals": schemas.Amt_Rotation_Totals,
    "rotation_inr_in": schemas.Rotation_INR_In,
    "rotation_usd_in": schemas.Rotation_USD_In
}

schema_id_assoc = {
    "alloc": "account",
    "burn": "burn_id",
    "fss_burn": "fss_burn_id",
    "rotation_totals": "amt_rotation_id",
    "rotation_inr_in": "inr_rotation_id",
    "rotation_usd_in": "usd_rotation_id"
}

valid_filters = ["burn_account", "burn_date", "burn_title"]


# generate date/datetime string
'''
    %Y = Year
    %m = month (01-12)
    %d = date (01-31)
    %H = Hour (00-23)
    %M = Minute (00-59)
    %S = Second (00-59)
'''
def get_curdate_str(type_arg: str | None = None) -> str:
    if type_arg is not None:
        type_arg = type_arg.upper() 
    now = datetime.now()
    default_res = now.strftime("%Y%m%d%H%M%S")
    if type_arg == 'D':
        result = now.strftime("%Y%m%d")
    else:
        result = default_res
    return result

def validate_filters(filters: Dict[str, Any]):
    invalid = []
    for key in filters.keys():
        if key not in valid_filters:
            invalid.append(key)
    if len(invalid) > 0:
        raise Filter_Validation_Exception(filters=invalid)
    else:
        print("All Filters Valid!")
    
# Insert default row to rotation_totals
def insert_default_row(target, connection, **kwargs):
    default_row = {
        "amt_rotation_id": "amt_rot_default", # Take this (wherever it is referred) from env
        "inr_in": 0,
        "inr_out": 0,
        "usd_in": 0,
        "usd_out": 0,
        "inr_rot_bal": 0,
        "usd_rot_bal": 0
    }
    table = schemas.Amt_Rotation_Totals
    try:
        exist = connection.execute(select(table).where(table.amt_rotation_id == "amt_rot_default")).fetchone()
        if exist is None or len(exist)<=0:
            connection.execute(insert(table).values(default_row))
            print("Defaults Created!")
        else:
            print("Defaults Already Exist, Skipping Defaults!")
    except Exception as e:
        print("Defaults Creation Failed, Please Add Manually!")