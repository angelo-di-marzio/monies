#!/usr/bin/env python3
from sqlalchemy.orm import Session
from model.user import User
from . import schema
from services.queue.rabbit import add_to_queue


def get_user(db: Session, user_id: int):
    return db.query(schema.User).filter(schema.User.id == user_id).first()


def get_user_by_mail(db: Session, email: str):
    return db.query(schema.User).filter(schema.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schema.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: User):
    db_user = schema.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(schema.User).filter(schema.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return


def update_user(db: Session, user: User):
    old_user_query = db.query(schema.User).filter(schema.User.id == user.id)
    old_user = old_user_query.first()

    # if user.accounts is an empty array, SQLAlechemy raises an error
    if len(user.accounts) == 0:
        del user.accounts

    old_user_query.update(user.dict())
    db.commit()
    db.refresh(old_user)
    return old_user
