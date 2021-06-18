"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class ListItem(db.Document):
    """Data model for Grocery Item List of a User."""
    id = db.SequenceField(primary_key=True, required=True)
    list_id = db.IntField(required=True)
    item_id = db.IntField(required=True)
    item_qty = db.DecimalField(required=True)
    created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<List Items {}>'.format(self.list_itm_name)