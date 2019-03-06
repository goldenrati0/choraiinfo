import enum
from datetime import datetime
from typing import List, Dict, Any

import bcrypt
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID, JSON

from src.utilities import Generator
from .base import db, BaseModel


class UserLevelEnum(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super-admin"


class User(BaseModel, db.Model):
    __tablename__ = "user"

    uid = db.Column(UUID, primary_key=True, default=Generator.uuid)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    _phones = db.Column(JSON, default=[])
    _address = db.Column(JSON, default={})
    _user_level = db.Column(Enum(UserLevelEnum), default=UserLevelEnum.USER)
    joined_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username: str, email: str, password: str, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        self.email = email
        self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def __str__(self):
        return self.__repr__()

    def update(self, **kwargs):
        self._phones = kwargs.get("phones")
        self._address = kwargs.get("address")
        return self.save()

    @staticmethod
    def update_all(users: List, **kwargs):
        for user in users:
            user.update(**kwargs)

    @property
    def phones(self) -> List[str]:
        return self._phones

    @property
    def address(self) -> Dict[str, Any]:
        return self._address
