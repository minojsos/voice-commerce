"""Data models."""
import sys
import os
import datetime
from flask_mongoengine import MongoEngine
sys.path.append("...")
import db

class Shop(db.Document):
    """Data model for shops."""

    __tablename__ = 'shop'
    shop_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shop_name = db.Column(
        db.String(255),
        index=False,
        unique=False,
        nullable=False
    )

    shop_phone = db.Column(
        db.String(255),
        index=True,
        unique=True,
        nullable=False
    )

    shop_address = db.Column(
        db.Unicode(1000),
        index=False,
        unique=False,
        nullable=False
    )

    shop_email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )

    shop_lat = db.Column(
        db.Unicode(1000),
        index=False,
        unique=False,
        nullable=False,
    )
    
    shop_long = db.Column(
        db.Unicode(1000),
        index=False,
        unique=False,
        nullable=False,
    )

    shop_available = db.Column(
        db.Integer(),
        index=False,
        unique=False,
        nullable=False,
        default=1
    )

    shop_created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    shop_updated_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=None
    )

    def __repr__(self):
        return '<Shop {}>'.format(self.shop_name)