"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
import db

class Order(db.Document):
    """Data model for Caet orders."""
    order_id = db.SequenceField(primary_key=True, required=True)
    order_status = db.IntField(required=True, default=0) # 0=> Processing, 1 => Completed, 2 => Cancelled
    order_created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    order_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Orders {}>'.format(self.corder_id)