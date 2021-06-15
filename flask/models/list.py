"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
import db

class List(db.Document):
    """Data model for Grocery Item List of a User."""
    list_id = db.SequenceField(primary_key=True)
    user_id = db.IntField(required=True)
    item_created_on = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    item_updated_on = db.DateTimeField(default=None)
    
    __tablename__ = 'list'
    list_id = db.Column(
        db.Integer,
        primary_key=True
    )

    list_itm_name = db.Column(
        db.String(50),
        index=False,
        unique=False,
        nullable=False
    )

    list_itm_qty = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )

    list_itm_unit = db.Column(
        db.String(50),
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<List Items {}>'.format(self.list_itm_name)