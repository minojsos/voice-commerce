"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class Order(db.Document):
    """Data model for Caet orders."""
    order_id = db.SequenceField(primary_key=True, required=True)
    shop_id = db.IntField(required=True, default=0)
    user_id = db.IntField(required=True)
    coupon_id = db.IntField(required=True)
    coupon_value = db.DecimalField(required=True)
    order_status = db.IntField(required=True, default=0) # 0=> Processing, 1 => Completed, 2 => Cancelled, 3 => Returned
    order_payment = db.IntField(required=True, default=0) # 0=> COD, 1 => CARD
    cancel_reason = db.StringField(required=False, default="")
    return_reason = db.StringField(required=False, default="")
    review_reason = db.StringField(required=False, default="")
    address = db.StringField(required=True)
    order_created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    order_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Orders {}>'.format(self.order_id)