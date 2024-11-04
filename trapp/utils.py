from datetime import datetime
import json
import os
from sqlalchemy import insert, select
from typing import Any, Dict
from .exceptions import Filter_Validation_Exception
from . import schemas

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
    default_res = now.strftime(get_env_var("default_datetime_format"))
    if type_arg == 'D':
        result = now.strftime(get_env_var("default_date_format"))
    else:
        result = default_res
    return result

def validate_filters(filters: Dict[str, Any]):
    valid_filters = get_env_var("valid_filters").split(",")
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
    amt_rotation_id_val = get_env_var("def_rot_tot_id")
    default_row = json.loads(get_env_var("amt_totals_default_row"))
    table = schemas.Amt_Rotation_Totals
    try:
        exist = connection.execute(select(table).where(table.amt_rotation_id == amt_rotation_id_val)).fetchone()
        if exist is None or len(exist)<=0:
            connection.execute(insert(table).values(default_row))
            print("Defaults Created!")
        else:
            print("Defaults Already Exist, Skipping Defaults!")
    except Exception as e:
        print("Defaults Creation Failed, Please Add Manually!")
        
# ENV Getter
def get_env_var(env_key):
    if not os.getenv("DEPENV"):
        from dotenv import load_dotenv
        load_dotenv()
    return os.getenv(env_key)