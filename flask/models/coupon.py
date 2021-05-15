"""Data models."""
from . import db
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table

class Coupon(db.Model):
    """Data model for coupons."""

    __tablename__ = 'shop'
    coupon_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shop_id = db.Column(
        db.Integer,
        ForeignKey('shop.shop_id'),
    )

    coupon_value = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )

    coupon_available = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False,
        default=1
    )

    coupon_created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    coupon_updated_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=None
    )

    def __repr__(self):
        return '<Coupon {}>'.format(self.coupon_value)