"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class StoreList(db.Document):
    """Data model for items."""
    storeList_id = db.SequenceField(primary_key=True)
    user_id = db.StringField(required=True)
    item_ids = db.ListField(db.StringField())
    item_created_on = db.DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<List Items {}>'.format(self.storeList_id)