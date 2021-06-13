"""Data models."""
from . import db
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table

class Corder(db.Model):
    """Data model for Caet orders."""

    __tablename__ = 'corder'
    corder_id = db.Column(
        db.Integer,
        primary_key=True
    )

    cart_id = db.Column(
        db.Integer,
        ForeignKey('cart.cart_id'),
    )

    corder_status = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False,
        default=1
    )

    corder_created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    corder_updated_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=None
    )

    def __repr__(self):
        return '<Orders {}>'.format(self.corder_id)