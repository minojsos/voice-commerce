"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
import db

class OrderItem(db.Document):
    """Data model for Caet orders."""
    id = db.SequenceField(primary_key=True, required=True)
    order_id = db.IntField(required=True)
    item_id = db.IntField(required=True)
    item_name = db.StringField(required=True)
    item_code = db.StringField(required=True)
    item_rate = db.StringField(required=True)
    item_offer_price = db.DecimalField(required=False,default=None)
    item_qty = db.DecimalField(required=True)
    created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Orders {}>'.format(self.corder_id)