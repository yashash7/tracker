from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from typing import Dict, Any
from .service import Fetcher_Service, Adder_Service
from .dbc import init_db
from . import models
from .utils import validate_filters
from .exceptions import Filter_Validation_Exception

app = FastAPI(title='TrApp')

app.add_event_handler("startup", init_db)

# Initialize Services
fetcher = Fetcher_Service()
adder = Adder_Service()

@app.get("/", include_in_schema=False)
async def home():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="TrApp | Documentation")

@app.get("/getalls")
async def get_all_by_schema(schema_type):
    return fetcher.fetch_all_by_schema(schema_type)

@app.get("/anybyid")
async def get_any_by_id(schema_type: str, id: str):
    return fetcher.fetch_any_by_id(schema_type, id)

@app.post("/addalloc")
async def add_new_alloc(alloc: models.Alloc_Create):
    return adder.add_alloc(alloc)

@app.post("/addburn")
async def add_new_burn(burn: models.Burn_Create):
    return adder.add_burn(burn)

@app.post("/filterfetch")
async def get_filtered_alls(filters: Dict[str, Any], schema_type):
    validate_filters(filters)
    return fetcher.filtered_fetch(schema_type, filters)

# Error Handlers
@app.exception_handler(Filter_Validation_Exception)
async def handle_filter_validation_exception(req: Request, e: Filter_Validation_Exception):
    return JSONResponse(
        status_code=400,
        content=e.__dict__
    )