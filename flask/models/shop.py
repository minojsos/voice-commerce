"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class Shop(db.Document):
    """Data model for shops."""
    shop_id = db.SequenceField(primary_key=True, required=True)
    shop_name = db.StringField(required=True)
    shop_phone = db.StringField(required=True)
    shop_address = db.StringField(required=True)
    shop_email = db.StringField(required=True)
    shop_lat = db.DecimalField(required=True)
    shop_long = db.DecimalField(required=True)
    shop_available = db.IntField(required=True, default=1) # 0=> Unavailable 1=> Available
    shop_created_on = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
    shop_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Shop {}>'.format(self.shop_name)