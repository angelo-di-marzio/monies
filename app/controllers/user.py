#!/usr/bin/env python3
from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.user import User, UserBase
from services.database.user import (
    get_user,
    get_users,
    create_user,
    delete_user,
    update_user,
)
from services.queue.rabbit import add_to_queue
from services.user import validate_user_id, validate_user_email


def create(db: Session, user: UserBase):
    if not validate_user_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user)
    # add user_id to the queue for address processing
    if new_user.address and new_user.address.strip() != "":
        add_to_queue(new_user.id)
    return new_user


def get_one(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return get_users(db, skip=skip, limit=limit)


def delete(db: Session, user_id: int):
    if not validate_user_id(db, user_id):
        raise HTTPException(status_code=404, detail="Not found")
    return delete_user(db, user_id)


def update(db: Session, user: User):
    old_user = get_user(db, user.id)
    if not old_user:
        raise HTTPException(status_code=404, detail="Not found")

    # check if new address
    if user.address and user.address.strip() != old_user.address.strip():
        add_to_queue(user.id)

    new_user = update_user(db, user)
    return new_user
