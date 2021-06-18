"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from routes import *

class UserCoupon(db.Document):
    """Data model for user coupons."""
    id = db.SequenceField(primary_key=True)
    user_id = db.IntField(required=True)
    coupon_id = db.IntField(required=True)
    coupon_value = db.DecimalField(required=True)
    coupon_available = db.DecimalField(required=True)
    user_created_on = db.DateTimeField(default=datetime.datetime.utcnow)
    user_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)