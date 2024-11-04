from sqlalchemy import Column, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .enums import EXCHANGE

Base = declarative_base()

class Alloc(Base):
    __tablename__ = 'total_allocs'
    account = Column(String(7), primary_key = True, index = True)
    alloc_amt = Column(Float)
    base_amt = Column(Float)
    chrg_amt = Column(Float)
    bal_amt = Column(Float)
    #Relation
    burns = relationship("Burn", back_populates="alloc")

class Burn(Base):
    __tablename__ = 'burn_details'
    burn_id = Column(String(14), primary_key = True, index = True)
    burn_title = Column(String(70), index = True)
    burn_base_amt = Column(Float)
    burn_chrg_amt = Column(Float)
    burn_total_amt = Column(Float)
    burn_date = Column(String(14), index = True)
    #Relation
    burn_account = Column(String(7), ForeignKey('total_allocs.account'))
    alloc = relationship("Alloc", back_populates="burns")
    fss_burns = relationship("FSS_Burn", back_populates="burn")

class FSS_Burn(Base): # Child Table to Burn (for types shop, food, supplies)
    __tablename__ = 'fss_burn_details'
    fss_burn_id = Column(String(14), primary_key = True, index = True)
    fss_burn_title = Column(String(70), index = True)
    fss_burn_amt = Column(Float)
    #Relation
    burn_id = Column(String(14), ForeignKey('burn_details.burn_id'))
    burn = relationship("Burn", back_populates="fss_burns")

class Amt_Rotation_Totals(Base):
    __tablename__ = 'amt_rotation_totals'
    amt_rotation_id = Column(String(15), primary_key = True, index = True)
    inr_in = Column(Float)
    inr_out = Column(Float)
    usd_in = Column(Float)
    usd_out = Column(Float)
    inr_rot_bal = Column(Float)
    usd_rot_bal = Column(Float)

class Rotation_INR_In(Base):
    __tablename__ = 'rotation_inr_in'
    inr_rotation_id = Column(String(14), primary_key = True, index = True)
    usd_out_to = Column(String(50), index = True)
    usd_amt = Column(Float)
    inr_amt = Column(Float)
    paid_day_rate = Column(Float)
    settled_day_rate = Column(Float)
    paid_day = Column(String(14), index = True)
    settled_day = Column(String(14), index = True)
    usd_out_type = Column(String(25), index = True)
    comments = Column(String(250))


class Rotation_USD_In(Base):
    __tablename__ = 'rotation_usd_in'
    usd_rotation_id = Column(String(14), primary_key = True, index = True)
    inr_out_to = Column(String(50), index = True)
    usd_amt = Column(Float)
    inr_amt = Column(Float)
    paid_day_rate = Column(Float)
    settled_day_rate = Column(Float)
    paid_day = Column(String(14), index = True)
    settled_day = Column(String(14), index = True)
    inr_out_type = Column(String(25), index = True)
    comments = Column(String(250))

class Cash_Exchange(Base):
    __tablename__ = "cash_exchange"
    exchange_id = Column(String(14), primary_key = True, index = True)
    to_or_from = Column(String(50), index = True)
    paid_cash_amt = Column(Float)
    paid_online_amt = Column(Float)
    got_cash_amt = Column(Float)
    got_online_amt = Column(Float)
    exchange_type = Column(Enum(EXCHANGE), index = True)
    paid_currency = Column(String(10), index = True)
    got_currency = Column(String(10), index = True)
    exchange_Date = Column(String(14), index = True)
    burn_id = Column(String(14), index = True)