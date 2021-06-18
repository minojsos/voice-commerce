"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class List(db.Document):
    """Data model for Grocery Item List of a User."""
    list_id = db.SequenceField(primary_key=True)
    user_id = db.IntField(required=True)
    item_created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    item_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<List Items {}>'.format(self.list_itm_name)