from sqlalchemy.orm import Session
from .schemas import *

'''def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()'''

'''def create_item(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item'''

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
        db.commit()
    except Exception as e:
        raise e
