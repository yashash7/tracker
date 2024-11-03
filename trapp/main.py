from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from typing import Dict, Any, Union, List
from sqlalchemy import event
from .schemas import Amt_Rotation_Totals
from .service import Fetcher_Service, Adder_Service
from .dbc import init_db
from . import models
from . import utils
from .exceptions import Filter_Validation_Exception

app = FastAPI(title='TrApp')

app.add_event_handler("startup", init_db)

# Initialize Services
fetcher = Fetcher_Service()
adder = Adder_Service()

@app.get("/", include_in_schema=False)
async def home():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="TrApp | Documentation")

@app.get("/getalls", response_model = List[Union[models.Alloc_Base, models.Burn_Base, models.FSS_Burn_Base, models.Amt_Rotation_Totals_Base, models.Rotation_INR_In_Base, models.Rotation_USD_In_Base]])
async def get_all_by_schema(schema_type):
    return fetcher.fetch_all_by_schema(schema_type)

@app.get("/getanybyid", response_model=Union[models.Alloc_Base, models.Burn_Base, models.FSS_Burn_Base, models.Amt_Rotation_Totals_Base, models.Rotation_INR_In_Base, models.Rotation_USD_In_Base])
async def get_any_by_id(schema_type: str, id: str):
    return fetcher.fetch_any_by_id(schema_type, id)

@app.post("/filterfetch", response_model=List[Union[models.Alloc_Base, models.Burn_Base, models.FSS_Burn_Base, models.Amt_Rotation_Totals_Base, models.Rotation_INR_In_Base, models.Rotation_USD_In_Base]])
async def get_filtered_alls(filters: Dict[str, Any], schema_type):
    utils.validate_filters(filters)
    return fetcher.filtered_fetch(schema_type, filters)

@app.post("/addalloc", response_model=models.Alloc_Create)
async def add_new_alloc(alloc: models.Alloc_Create):
    return adder.add_alloc(alloc)

@app.post("/addburn", response_model=models.Burn_Create)
async def add_new_burn(burn: models.Burn_Create):
    return adder.add_burn(burn)

@app.post("/addfssburn", response_model=models.FSS_Burn_Create)
async def add_new_fss_burn(fss_burn: models.FSS_Burn_Create):
    return adder.add_fss_burn(fss_burn)

@app.post("/addinrin", response_model=models.Rotation_INR_In_Create)
async def add_new_rot_inr_in(inr_in: models.Rotation_INR_In_Create):
    return adder.add_rot_inr_in(inr_in)

@app.post("/addusdin", response_model=models.Rotation_USD_In_Create)
async def add_new_rot_usd_in(usd_in: models.Rotation_USD_In_Create):
    return adder.add_rot_usd_in(usd_in)


# Exception Handlers
@app.exception_handler(Filter_Validation_Exception)
async def handle_filter_validation_exception(req: Request, e: Filter_Validation_Exception):
    return JSONResponse(
        status_code=400,
        content=e.__dict__
    )
    
# Events
event.listen(Amt_Rotation_Totals.__table__, "after_create", utils.insert_default_row)