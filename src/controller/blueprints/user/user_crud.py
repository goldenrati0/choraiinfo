from typing import Union, Tuple, Optional

from src.model import User


def create_new_user(username: str, email: str, password: str, **kwargs) -> Union[Tuple[User, bool], Tuple[str, bool]]:
    user = User(username=username, email=email, password=password, **kwargs)
    return user.save()


def get_user_from_id(uid: str) -> User:
    return User.query.get(uid)


def get_user_from_email(email: str) -> User:
    return User.query.filter(
        User.email == email
    ).first()


def user_check_credential(email: str, password: str) -> bool:
    user = get_user_from_email(email)
    if not user:
        return False
    return user.check_password(password)
