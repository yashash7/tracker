from . import schemas
from . import models

schema_type_assoc = {
    "alloc": schemas.Alloc,
    "burn": schemas.Burn,
    "fss_burn": schemas.FSS_Burn,
    "rotation_totals": schemas.Amt_Rotation_Totals,
    "rotation_inr_in": schemas.Rotation_INR_In,
    "rotation_usd_in": schemas.Rotation_USD_In,
    "cash_exchange": schemas.Cash_Exchange
}

response_models = (models.Alloc_Base, models.Burn_Base, models.FSS_Burn_Base, models.Amt_Rotation_Totals_Base, models.Rotation_INR_In_Base, models.Rotation_USD_In_Base, models.Cash_Exchange_Base)