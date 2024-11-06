from .auth import Interceptor, verify_access_token
from fastapi import Depends, FastAPI, Request as fapi_request
from fastapi.responses import JSONResponse
from sqlalchemy import event
from typing import Any, Dict, List, Union
from .commons import response_models
from .dbc import init_db
from .exceptions import Filter_Validation_Exception
from .schemas import Amt_Rotation_Totals
from .service import Adder_Service, Auth_Service, Fetcher_Service
from .utils import get_env_var, insert_default_row, validate_filters
from . import models

app_name = get_env_var("app_title", "TrApp")

app = FastAPI(title=app_name)

app.add_event_handler("startup", init_db)

app.add_middleware(Interceptor)

# Initialize Services
fetcher = Fetcher_Service()
adder = Adder_Service()
auth = Auth_Service()

@app.get("/")
async def home():
    return "Welcome to YcK's TrApp, for more information, please contact YcK - yck@svarpy.org"

# Login
@app.post("/login", response_model=models.Token)
async def login(user: models.User_Login):
    return auth.validate_login(user)

# Ping for client
@app.get("/ping")
async def ping(token: str = Depends(verify_access_token)):
    return -1 if not token else 1

@app.get("/getalls", response_model = List[Union[response_models]])
async def get_all_by_schema(schema_type):
    return fetcher.fetch_all_by_schema(schema_type)

@app.get("/getanybyid", response_model=Union[response_models])
async def get_any_by_id(schema_type: str, id: str):
    return fetcher.fetch_any_by_id(schema_type, id)

@app.post("/filterfetch", response_model=List[Union[response_models]])
async def get_filtered_alls(filters: Dict[str, Any], schema_type):
    validate_filters(filters)
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

@app.post("/addexchange", response_model=models.Cash_Exchange_Create)
async def add_new_exchange(exchange: models.Cash_Exchange_Create):
    return adder.add_exchange(exchange)


# Exception Handlers
@app.exception_handler(Filter_Validation_Exception)
async def handle_filter_validation_exception(req: fapi_request, e: Filter_Validation_Exception):
    return JSONResponse(
        status_code=400,
        content=e.__dict__
    )
    
# Events
event.listen(Amt_Rotation_Totals.__table__, "after_create", insert_default_row)