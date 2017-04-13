# coding: utf-8
"""

"""

import enum
import datetime

from .. import db

__author__ = 'Florian Rhiem <f.rhiem@fz-juelich.de>'


@enum.unique
class UserLogEntryType(enum.Enum):
    OTHER = 0
    CREATE_OBJECT = 1
    EDIT_OBJECT = 2
    EDIT_OBJECT_PERMISSIONS = 3
    REGISTER_USER = 4
    INVITE_USER = 5
    EDIT_USER_PREFERENCES = 6


class UserLogEntry(db.Model):
    __tablename__ = 'user_log_entries'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(UserLogEntryType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    utc_datetime = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref="log_entries")

    def __init__(self, type, user_id, data, utc_datetime=None):
        self.type = type
        self.user_id = user_id
        self.data = data
        if utc_datetime is None:
            utc_datetime = datetime.datetime.utcnow()
        self.utc_datetime = utc_datetime

    def __repr__(self):
        return '<{0}(id={1.id}, type={1.type}, user_id={1.user_id}, utc_datetime={1.utc_datetime}, data={1.data})>'.format(type(self).__name__, self)