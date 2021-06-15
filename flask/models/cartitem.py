"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
import db

class CartItem(db.Document):
    """Data model for carts."""
    id = db.SequenceField(primary_key=True)
    cart_id = db.IntField(required=True)
    item_id = db.IntField(required=True)
    item_name = db.StringField(required=True)
    item_code = db.StringField(required=True)
    item_rate = db.StringField(required=True)
    item_offer_price = db.DecimalField(required=False,default=None)
    item_qty = db.DecimalField(required=True)
    created_on = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Cart {}>'.format(self.cart_id)