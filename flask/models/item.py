"""Data models."""
from . import db
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table

class Item(db.Model):
    """Data model for items."""

    __tablename__ = 'item'
    item_id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_code = db.Column(
        db.String(50),
        index=False,
        unique=False,
        nullable=False
    )

    shop_id = db.Column(
        db.Integer,
        ForeignKey('shop.shop_id'),
    )

    item_name = db.Column(
        db.String(1000),
        index=False,
        unique=False,
        nullable=False
    )

    item_stock = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False,
        default=0
    )

    item_rate = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )

    item_unit = db.Column(
        db.String(50),
        index=False,
        unique=False,
        nullable=False
    )

    item_created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    item_updated_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=None
    )

    def __repr__(self):
        return '<Item {}>'.format(self.item_name)