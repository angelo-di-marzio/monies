#!/usr/bin/env python3
from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.account import Account, AccountBase
from services.database.account import (
    get_account,
    get_accounts,
    create_account,
    delete_account,
    update_account,
)
from services.account import validate_user_id, validate_account_id


def create(db: Session, account: AccountBase):
    if not validate_user_id(db, account):
        raise HTTPException(status_code=400, detail="Wrong owner_id !")
    return create_account(db, account)


def get_one(db: Session, account_id: int):
    account = get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Not found")
    return account


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return get_accounts(db, skip=skip, limit=limit)


def delete(db: Session, account_id: int):
    if not validate_account_id(db, account_id):
        raise HTTPException(status_code=400, detail="Wrong user id")
    return delete_account(db, account_id)


def update(db: Session, account: Account):
    old_account = get_account(db, account.id)
    if not old_account:
        raise HTTPException(status_code=404, detail="Not found")
    new_account = update_account(db, account)
    return new_account
