"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
from db import *

class User(db.Document):
    """Data model for user accounts."""
    user_id = db.SequenceField(primary_key=True)
    user_name = db.StringField(required=True)
    user_phone = db.StringField(required=True)
    user_email = db.StringField(required=True)
    user_address = db.StringField(required=True)
    user_lat = db.DecimalField(required=True)
    user_long = db.DecimalField(required=True)
    user_created_on = db.DateTimeField(default=datetime.datetime.utcnow)
    user_updated_on = db.DateTimeField(default=None)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)