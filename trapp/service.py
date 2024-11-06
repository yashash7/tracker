from contextlib import contextmanager
from fastapi import HTTPException
from .auth import create_access_token, verify_psd
from .commons import schema_type_assoc
from .dbc import SessionLocal
from .utils import get_env_var, processb64
from . import dbo
from . import models
from . import schemas

class Init_DB:

    @contextmanager
    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
            
class Auth_Service(Init_DB):
    
    def validate_login(self, user: models.User_Login):
        if not user.username or not user.password:
            raise HTTPException(status_code=400, detail="Both Username and Password are Required!")
        try:
            with self.get_db() as db:
                db_user = dbo.get_user(db, processb64(user.username))
        except Exception as e:
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        # Validate
        if not db_user or not verify_psd(processb64(user.password), db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials!")
        token = create_access_token(data={"subject": db_user.username})
        return models.Token(access_token=token, token_type="bearer")

class Fetcher_Service(Init_DB):

    def fetch_all_by_schema(self, schema_type):
        try:
            with self.get_db() as db:
                response = dbo.generic_fetch_all(db, schema_type_assoc.get(schema_type))
        except Exception as e:
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def fetch_any_by_id(self, schema_type, id):
        schema = schema_type_assoc.get(schema_type)
        id_col = get_env_var("schema_id_"+schema_type)
        try:
            with self.get_db() as db:
                response = dbo.generic_fetch_by_id(db, schema, id_col, id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def filtered_fetch(self, schema_type, filters):
        schema = schema_type_assoc.get(schema_type)
        try:
            with self.get_db() as db:
                response = dbo.generic_fetch_by_filters(db, schema, filters)
        except Exception as e:
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
                db.commit()
            response = new_item
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def add_burn(self, new_item: models.Burn_Create):
        burn_total = getattr(new_item, "burn_base_amt")+getattr(new_item, "burn_chrg_amt")
        setattr(new_item, "burn_total_amt", burn_total)
        entry = schemas.Burn()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        alloc_account = getattr(entry, "burn_account")
        if self.checker.check_existing("alloc", alloc_account) == 1:
            try:
                with self.get_db() as db:
                    dbo.generic_add(db, entry)
                    dbo.update_alloc(db, entry)
                    db.commit()
                response = new_item
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        else: 
            raise HTTPException(status_code=400, detail="Account - "+ alloc_account+ " does't exist!")
        return response
    
    def add_fss_burn(self, new_item: models.FSS_Burn_Create):
        entry = schemas.FSS_Burn()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        try:
            with self.get_db() as db:
                dbo.generic_add(db, entry)
                db.commit()
            response = new_item
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def add_rot_inr_in(self, new_item: models.Rotation_INR_In_Create):
        entry = schemas.Rotation_INR_In()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        try:
            with self.get_db() as db:
                dbo.generic_add(db, entry)
                dbo.update_rotation_totals(db, entry)
                db.commit()
            response = new_item
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def add_rot_usd_in(self, new_item: models.Rotation_USD_In_Create):
        entry = schemas.Rotation_USD_In()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        try:
            with self.get_db() as db:
                dbo.generic_add(db, entry)
                dbo.update_rotation_totals(db, entry)
                db.commit()
            response = new_item
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response
    
    def add_exchange(self, new_item: models.Cash_Exchange_Create):
        entry = schemas.Cash_Exchange()
        for key, value in new_item.__dict__.items():
            setattr(entry, key, value)
        try:
            with self.get_db() as db:
                dbo.generic_add(db, entry)
                db.commit()
            response = new_item
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=e.__cause__.__str__())
        return response