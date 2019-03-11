"""
Define an Abstract Base Class (ABC) for models
"""
from datetime import datetime
from typing import Union, Tuple

from sqlalchemy import inspect

from src.setup import db


class BaseModel():
    """ Generalize __init__, __repr__ and to_json
        Based on the models columns """

    def __repr__(self):
        """ Define a base way to print models
            Columns that start with _ are excluded """
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if not column.startswith("_")
        })

    @property
    def json(self):
        """ Define a base way to jsonify models
            Columns that start with _ are excluded """
        return {
            column: value
            if not isinstance(value, datetime) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
            if not column.startswith("_")
        }

    def _to_dict(self):
        """ This would more or less be the same as a `to_json`
            But putting it in a "private" function
            Allows to_json to be overriden without impacting __repr__
            Or the other way around
            And to add filter lists """
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self) -> Union[Tuple[db.Model, bool], Tuple[str, bool]]:
        try:
            db.session.add(self)
            db.session.commit()
            return self, False
        except Exception as ex:
            return str(ex), True

    def delete(self):
        db.session.delete(self)
        db.session.commit()
