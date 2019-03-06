import enum
from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from src.utilities import Generator
from .base import db, BaseModel


class ItemTypeEnum(enum.Enum):
    LAPTOP = "laptop"
    CELL_PHONE = "cell-phone"
    VEHICLE = "vehicle"


class LostItem(BaseModel):
    uid = db.Column(UUID, primary_key=True, default=Generator.uuid)
    item_type = db.Column(Enum(ItemTypeEnum), nullable=False)
    is_stolen = db.Column(db.Boolean, default=False, nullable=False)
    gd_copy_number = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    record_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)

    def __init__(self, item_type, **kwargs):
        super(LostItem, self).__init__(**kwargs)
        self.item_type = item_type
        if kwargs.get("is_stolen") is True:
            self.last_update = datetime.now()

    def __eq__(self, other):
        return isinstance(other, LostItem) \
               and self.uid == other.uid \
               and self.item_type == other.item_type


class Laptop(LostItem, db.Model):
    __tablename__ = "laptop"

    user_uid = db.Column(UUID, db.ForeignKey("user.uid"))
    serial_number = db.Column(db.String(255), unique=True, index=True, nullable=True)
    mac_address = db.Column(db.String(255), unique=True, index=True, nullable=True)

    # relationships
    owner = db.relationship("User", back_populates="laptops", lazy="joined")

    def __init__(self, user_uid: str, **kwargs):
        super(Laptop, self).__init__(ItemTypeEnum.LAPTOP, **kwargs)
        self.user_uid = user_uid
        self.serial_number = kwargs.get("serial_number")
        self.mac_address = kwargs.get("mac_address")

    def __eq__(self, other):
        return super(Laptop, self).__eq__(other) \
               and self.serial_number == other.serial_number \
               and self.mac_address == other.mac_address


class CellPhone(LostItem, db.Model):
    __tablename__ = "cellphone"

    user_uid = db.Column(UUID, db.ForeignKey("user.uid"))
    imei_1 = db.Column(db.String(100), unique=True, index=True, nullable=True)
    imei_2 = db.Column(db.String(100), unique=True, index=True, nullable=True)

    # relationships
    owner = db.relationship("User", back_populates="cell_phones", lazy="joined")

    def __init__(self, user_uid: str, **kwargs):
        super(CellPhone, self).__init__(ItemTypeEnum.CELL_PHONE, **kwargs)
        self.user_uid = user_uid
        self.imei_1 = kwargs.get("imei_1")
        self.imei_2 = kwargs.get("imei_2")

    def __eq__(self, other):
        return super(CellPhone, self).__eq__(other) \
               and self.imei_1 == other.imei_1 \
               and self.imei_2 == other.imei_2


class Vehicle(LostItem, db.Model):
    __tablename__ = "vehicle"

    user_uid = db.Column(UUID, db.ForeignKey("user.uid"))
    serial_number = db.Column(db.String(255), unique=True, index=True, nullable=True)
    engine_number = db.Column(db.String(255), unique=True, index=True, nullable=True)
    license_number = db.Column(db.String(255), unique=True, index=True, nullable=True)

    # relationships
    owner = db.relationship("User", back_populates="vehicles", lazy="joined")

    def __init__(self, user_uid, **kwargs):
        super(Vehicle, self).__init__(ItemTypeEnum.VEHICLE, **kwargs)
        self.user_uid = user_uid
        self.serial_number = kwargs.get("serial_number")
        self.engine_number = kwargs.get("engine_number")
        self.license_number = kwargs.get("license_number")

    def __eq__(self, other):
        return super(Vehicle, self).__eq__(other) \
               and self.serial_number == other.serial_number \
               and self.engine_number == other.engine_number \
               and self.license_number == other.license_number
