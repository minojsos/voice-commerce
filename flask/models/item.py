"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class Item(db.Document):
    """Data model for items."""
    item_id = db.SequenceField(primary_key=True)
    item_code = db.StringField(required=True)
    shop_id = db.IntField(required=True)
    item_name = db.StringField(required=True)
    item_stock = db.DecimalField(required=True)
    item_price = db.DecimalField(required=True)
    item_offer_price = db.DecimalField(required=False, default=None)
    item_unit = db.StringField(required=True)
    item_created_on = db.DateTimeField(default=datetime.datetime.utcnow)
    item_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Item {}>'.format(self.item_name)