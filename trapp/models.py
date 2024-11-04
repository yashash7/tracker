from pydantic import BaseModel, Field
from typing import List, Optional
from . import utils
from .enums import EXCHANGE

class Alloc_Base(BaseModel):
    account: str
    alloc_amt: Optional[float] = 0
    base_amt: Optional[float] = 0
    chrg_amt: Optional[float] = 0
    bal_amt: Optional[float] = 0
class Alloc_Create(Alloc_Base):
    pass
class Alloc(Alloc_Base):
    burns: List['Burn'] = []
    class Config:
        from_attributes = True


class Burn_Base(BaseModel):
    burn_id: str = Field(default_factory = utils.get_curdate_str)
    burn_title: str
    burn_base_amt: Optional[float] = 0
    burn_chrg_amt: Optional[float] = 0
    burn_total_amt: Optional[float] = 0
    burn_date: Optional[str] = None
    burn_account: str
class Burn_Create(Burn_Base):
    pass
class Burn(Burn_Base):
    fss_burns: List['FSS_Burn'] = []
    class Config:
        from_attributes = True


class FSS_Burn_Base(BaseModel):
    fss_burn_id: str = Field(default_factory = utils.get_curdate_str)
    fss_burn_title: str
    fss_burn_amt: Optional[float] = 0
    burn_id: str
class FSS_Burn_Create(FSS_Burn_Base):
    pass
class FSS_Burn(FSS_Burn_Base):
    class Config:
        from_attributes = True


class Amt_Rotation_Totals_Base(BaseModel):
    amt_rotation_id: str
    inr_in: Optional[float] = 0
    inr_out: Optional[float] = 0
    usd_in: Optional[float] = 0
    usd_out: Optional[float] = 0
    inr_rot_bal: Optional[float] = 0
    usd_rot_bal: Optional[float] = 0
class Amt_Rotation_Totals_Create(Amt_Rotation_Totals_Base):
    pass
class Amt_Rotation_Totals(Amt_Rotation_Totals_Base):
    class Config:
        from_attributes = True


class Rotation_INR_In_Base(BaseModel):
    inr_rotation_id: str = Field(default_factory = utils.get_curdate_str)
    usd_out_to: str
    usd_amt: Optional[float] = 0
    inr_amt: Optional[float] = 0
    paid_day_rate: Optional[float] = 0
    settled_day_rate: Optional[float] = 0
    paid_day: Optional[str] = None
    settled_day: Optional[str] = None
    usd_out_type: Optional[str] = None
    comments: Optional[str] = None
class Rotation_INR_In_Create(Rotation_INR_In_Base):
    pass
class Rotation_INR_In(Rotation_INR_In_Base):
    class Config:
        from_attributes = True


class Rotation_USD_In_Base(BaseModel):
    usd_rotation_id: str = Field(default_factory = utils.get_curdate_str)
    inr_out_to: str
    usd_amt: Optional[float] = 0
    inr_amt: Optional[float] = 0
    paid_day_rate: Optional[float] = 0
    settled_day_rate: Optional[float] = 0
    paid_day: Optional[str] = None
    settled_day: Optional[str] = None
    inr_out_type: Optional[str] = None
    comments: Optional[str] = None
class Rotation_USD_In_Create(Rotation_USD_In_Base):
    pass
class Rotation_USD_In(Rotation_USD_In_Base):
    class Config:
        from_attributes = True

class Cash_Exchange_Base(BaseModel):
    exchange_id: str = Field(default_factory = utils.get_curdate_str)
    to_or_from: str
    paid_cash_amt: Optional[float] = 0
    paid_online_amt: Optional[float] = 0
    got_cash_amt: Optional[float] = 0
    got_online_amt: Optional[float] = 0
    exchange_type: EXCHANGE = Field(default_factory = lambda: EXCHANGE.PaidCash)
    paid_currency: Optional[str] = None
    got_currency: Optional[str] = None
    exchange_Date: Optional[str] = None
    burn_id: Optional[str] = None
class Cash_Exchange_Create(Cash_Exchange_Base):
    pass
class Cash_Exchange(Cash_Exchange_Base):
    class Config:
        from_attributes = True