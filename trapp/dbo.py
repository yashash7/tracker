from sqlalchemy.orm import Session
from typing import Union
from .schemas import *
from .utils import get_env_var

def generic_fetch_all(db: Session, schema):
    return db.query(schema).all()

def generic_fetch_by_id(db: Session, schema, id_col, id_val):
    return db.query(schema).filter(getattr(schema, id_col) == id_val).first()

def generic_fetch_by_filters(db: Session, schema, filters):
    filter_query = db.query(schema).filter_by(**filters)
    return filter_query.all()

def generic_add(db: Session, entry):
    try:
        db.add(entry)
    except Exception as e:
        raise e

def update_alloc(db: Session, entry: Burn):
    try:
        alloc_account: Alloc = generic_fetch_by_id(db, Alloc, get_env_var("schema_id_alloc"), entry.burn_account)
        if alloc_account:
            alloc_account.base_amt = alloc_account.base_amt + entry.burn_base_amt
            alloc_account.chrg_amt = alloc_account.chrg_amt + entry.burn_chrg_amt
            alloc_account.bal_amt = alloc_account.alloc_amt - (alloc_account.base_amt + alloc_account.chrg_amt)
    except Exception as e:
        raise e
    
def update_rotation_totals(db: Session, entry: Union[Rotation_INR_In, Rotation_USD_In]):
    schema = Amt_Rotation_Totals
    try:
        rot_totals: Amt_Rotation_Totals = generic_fetch_by_id(db, schema, get_env_var("schema_id_rotation_totals"), get_env_var("def_rot_tot_id"))
        if isinstance(entry, Rotation_INR_In):
            # INRIN-USDOUT
            rot_totals.inr_in += entry.inr_amt
            rot_totals.usd_out += entry.usd_amt
        else:
            # USDIN-INROUT
            rot_totals.usd_in += entry.usd_amt
            rot_totals.inr_out += entry.usd_amt
        rot_totals.inr_rot_bal = rot_totals.inr_in-rot_totals.inr_out
        rot_totals.usd_rot_bal = rot_totals.usd_in-rot_totals.usd_out
    except Exception as e:
        raise e
        