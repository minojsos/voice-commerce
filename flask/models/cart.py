"""Data models."""
from . import db
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table

class Item(db.Model):
    """Data model for carts."""

    __tablename__ = 'cart'
    cart_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shop_id = db.Column(
        db.Integer,
        ForeignKey('shop.shop_id'),
    )

    user_id = db.Column(
        db.Integer,
        ForeignKey('user.user_id'),
    )

    cart_created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    cart_updated_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=None
    )

    def __repr__(self):
        return '<Cart {}>'.format(self.cart_id)