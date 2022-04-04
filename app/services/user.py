#!/usr/bin/env python3
from sqlalchemy.orm import Session
from model.user import UserBase
from services.database.user import get_user, get_user_by_mail


def validate_user_email(db: Session, email: str):
    user = get_user_by_mail(db, email)
    print(user)
    if user:
        return False
    return True


def validate_user_id(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False
    return True
