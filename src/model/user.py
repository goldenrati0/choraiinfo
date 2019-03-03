from typing import List, Dict, Any

import bcrypt
from sqlalchemy.dialects.postgresql import UUID, JSON

from src.utilities import Generator
from .base import db, BaseModel, MetaBaseModel


class User(db.Model, BaseModel, metaclass=MetaBaseModel):
    __tablename__ = "user"

    uid = db.Column(UUID, primary_key=True, default=Generator.uuid)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    _phones = db.Column(JSON, default=[])
    _address = db.Column(JSON, default={})

    def __init__(self, username: str, email: str, password: str, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        self.email = email
        self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @property
    def phones(self) -> List[str]:
        return self._phones

    @property
    def address(self) -> Dict[str, Any]:
        return self._address
