from uuid import uuid4


class Generator:
    @staticmethod
    def uuid() -> str:
        return uuid4().hex
