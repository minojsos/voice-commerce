"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class Cart(db.Document):
    """Data model for carts."""
    cart_id = db.SequenceField(primary_key=True)
    shop_id = db.IntField(required=True,default=1)
    user_id = db.IntField(required=True)
    coupon_id = db.IntField(default=None)
    cart_created_on = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
    cart_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Cart {}>'.format(self.cart_id)