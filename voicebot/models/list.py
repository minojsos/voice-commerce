"""Data models."""
from . import db
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table

class List(db.Model):
    """Data model for Grocery Item List of a User."""

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
        return '<List Items {}>'.format(self.list_itm_name)