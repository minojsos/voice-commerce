"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class Coupon(db.Document):
    """Data model for coupons."""
    coupon_id = db.SequenceField(primary_key=True)
    coupon_value = db.DecimalField(required=True)
    shop_id = db.IntField(required=True)
    coupon_available = db.IntField(required=True) # 0 - unavailable, 1 - available
    coupon_created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    coupon_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Coupon {}>'.format(self.coupon_value)