"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class Category(db.Document):
    """Data model for carts."""
    category_id = db.SequenceField(primary_key=True)
    category_name = db.StringField(required=True)
    created_on = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<Cart {}>'.format(self.cart_id)