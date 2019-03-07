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
    """
        CREATE TABLE "user" (
            uid UUID NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            _password VARCHAR(128) NOT NULL,
            _phones JSON,
            _address JSON,
            _user_level userlevelenum NOT NULL,
            joined_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            PRIMARY KEY (uid)
        )
    """
    __tablename__ = "user"

    uid = db.Column(UUID, primary_key=True, default=Generator.uuid)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    _phones = db.Column(JSON, default=[], nullable=True)
    _address = db.Column(JSON, default={}, nullable=True)
    _user_level = db.Column(Enum(UserLevelEnum), default=UserLevelEnum.USER, nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # relationships
    laptops = db.relationship("Laptop", back_populates="owner", lazy="joined")
    cell_phones = db.relationship("CellPhone", back_populates="owner", lazy="joined")
    vehicles = db.relationship("Vehicle", back_populates="owner", lazy="joined")

    def __init__(self, username: str, email: str, password: str, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        self.email = email
        self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def __eq__(self, other):
        return self.uid == other.uid

    def __str__(self):
        return self.__repr__()

    def check_password(self, password: str) -> bool:
        return password is not None \
               and password != "" \
               and bcrypt.checkpw(password.encode(), self._password.encode())

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
