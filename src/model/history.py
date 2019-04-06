from datetime import datetime
from typing import List

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from src.utilities import Generator
from .base import db, BaseModel
from .lost_item import ItemTypeEnum, LostItem, Laptop, CellPhone, Vehicle


class SearchHistory(BaseModel, db.Model):
    __tablename__ = "search_history"

    uid = db.Column(UUID, primary_key=True, default=Generator.uuid)
    item_type = db.Column(Enum(ItemTypeEnum), nullable=False)
    search_string = db.Column(db.Text, nullable=False)
    search_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, item_type, search_string: str, **kwargs):
        super(SearchHistory, self).__init__(**kwargs)
        self.item_type = item_type
        self.search_string = search_string

    def matched_items(self) -> List[LostItem]:
        items: List[LostItem] = list()
        if self.item_type == ItemTypeEnum.LAPTOP:
            laptops = Laptop.query.filter(
                (Laptop.mac_address.ilike(f"%{self.search_string}%")) |
                (Laptop.serial_number.ilike(f"%{self.search_string}%")) |
                (Laptop.gd_copy_number.ilike(f"%{self.search_string}%")) |
                (Laptop.remarks.ilike(f"%{self.search_string}%"))
            ).all()
            items.extend(laptops)
        elif self.item_type == ItemTypeEnum.CELL_PHONE:
            phones = CellPhone.query.filter(
                (CellPhone.gd_copy_number.ilike(f"%{self.search_string}%")) |
                (CellPhone.imei_1.ilike(f"%{self.search_string}%")) |
                (CellPhone.imei_2.ilike(f"%{self.search_string}%")) |
                (CellPhone.remarks.ilike(f"%{self.search_string}%"))
            ).all()
            items.extend(phones)
        elif self.item_type == ItemTypeEnum.VEHICLE:
            vehicles = Vehicle.query.filter(
                (Vehicle.gd_copy_number.ilike(f"%{self.search_string}%")) |
                (Vehicle.serial_number.ilike(f"%{self.search_string}%")) |
                (Vehicle.engine_number.ilike(f"%{self.search_string}%")) |
                (Vehicle.license_number.ilike(f"%{self.search_string}%")) |
                (Vehicle.remarks.ilike(f"%{self.search_string}%"))
            ).all()
            items.extend(vehicles)

        return items

    @property
    def json(self):
        return {
            "uid": self.uid,
            "item_type": self.item_type,
            "search_string": self.search_string,
            "search_time": str(self.search_time),
            "matched_items": {
                self.item_type: [item.json for item in self.matched_items()]
            }
        }
