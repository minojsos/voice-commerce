"""Data models."""
from . import db
import datetime
from sqlalchemy import Column, Integer, DateTime


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'user'
    user_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_name = db.Column(
        db.String(255),
        index=False,
        unique=False,
        nullable=False
    )

    user_phone = db.Column(
        db.String(255),
        index=True,
        unique=True,
        nullable=False
    )

    user_email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )

    user_password = db.Column(
        db.String(255),
        index=False,
        unique=False,
        nullable=False,
    )

    user_address = db.Column(
        db.Unicode(1000),
        index=False,
        unique=False,
        nullable=False
    )

    user_created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    user_updated_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=None
    )

    def __repr__(self):
        return '<User {}>'.format(self.user_name)