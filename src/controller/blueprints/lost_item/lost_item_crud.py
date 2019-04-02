from typing import Optional

from src.model import SearchHistory, ItemTypeEnum, LostItem, Vehicle, Laptop, CellPhone
from src.setup import db


def add_search_history_vehicle(string: str) -> SearchHistory:
    sh = SearchHistory(ItemTypeEnum.VEHICLE, string)
    db.session.add(sh)
    db.session.commit()
    return sh


def add_search_history_laptop(string: str) -> SearchHistory:
    sh = SearchHistory(ItemTypeEnum.LAPTOP, string)
    db.session.add(sh)
    db.session.commit()
    return sh


def add_search_history_phone(string: str) -> SearchHistory:
    sh = SearchHistory(ItemTypeEnum.CELL_PHONE, string)
    db.session.add(sh)
    db.session.commit()
    return sh


def add_item(user_id, type: ItemTypeEnum, **kwargs) -> Optional[LostItem]:
    item = None
    if type == ItemTypeEnum.VEHICLE:
        item = Vehicle(user_id, **kwargs)
    elif type == ItemTypeEnum.LAPTOP:
        item = Laptop(user_id, **kwargs)
    elif type == ItemTypeEnum.CELL_PHONE:
        item = CellPhone(user_id, **kwargs)

    if not item:
        return None

    db.session.add(item)
    db.session.commit()
    return item
