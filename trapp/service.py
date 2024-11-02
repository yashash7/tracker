from contextlib import contextmanager
from fastapi import HTTPException
from .dbc import SessionLocal
from . import dbo
from . import schemas
from . import models
from .utils import schema_type_assoc, schema_id_assoc

class Init_DB:

    @contextmanager
    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

class Fetcher_Service(Init_DB):

    def fetch_all_by_schema(self, schema_type):
        try:
            with self.get_db() as db:
                response = dbo.generic_fetch_all(db, schema_type_assoc.get(schema_type))
        except Exception as e:
            response = HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def fetch_any_by_id(self, schema_type, id):
        schema = schema_type_assoc.get(schema_type)
        id_col = schema_id_assoc.get(schema_type)
        try:
            with self.get_db() as db:
                response = dbo.generic_fetch_by_id(db, schema, id_col, id)
                print("YcK: ", response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def filtered_fetch(self, schema_type, filters):
        schema = schema_type_assoc.get(schema_type)
        try:
            with self.get_db() as db:
                response = dbo.generic_fetch_by_filters(db, schema, filters)
        except Exception as e:
            print("YcKEX: ", e)
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
class Checker_Service(Fetcher_Service):
    
    def check_existing(self, schema_type, id):
        exist = self.fetch_any_by_id(schema_type, id)
        return -1 if exist is None else 1
    
class Adder_Service(Init_DB):
    
    def __init__(self):
        self.checker = Checker_Service()

    def add_alloc(self, new_item: models.Alloc_Create):
        bal = getattr(new_item, "alloc_amt") - (getattr(new_item, "base_amt")+getattr(new_item, "chrg_amt"))
        setattr(new_item, "bal_amt", bal)
        entry = schemas.Alloc()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        try:
            with self.get_db() as db:
                dbo.generic_add(db, entry)
                response = new_item
        except Exception as e:
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def add_burn(self, new_item: models.Burn_Create):
        total = getattr(new_item, "burn_base_amt")+getattr(new_item, "burn_chrg_amt")
        setattr(new_item, "burn_total_amt", total)
        entry = schemas.Burn()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        alloc_account = getattr(entry, "burn_account")
        if self.checker.check_existing("alloc", alloc_account) == 1:
            try:
                with self.get_db() as db:
                    dbo.generic_add(db, entry)
                    response = new_item
            except Exception as e:
                raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        else: 
            raise HTTPException(status_code=400, detail="Account - "+ alloc_account+ " does't exist!")
        return response


