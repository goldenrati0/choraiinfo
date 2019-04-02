from src.model import SearchHistory, ItemTypeEnum
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
