#!/usr/bin/env python3
from sqlalchemy.orm import Session
from model.account import Account
from . import schema


def get_account(db: Session, account_id: int):
    return db.query(schema.Account).filter(schema.Account.id == account_id).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schema.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: Account):
    db_account = schema.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def delete_account(db: Session, account_id: int):
    db_account = (
        db.query(schema.Account).filter(schema.Account.id == account_id).first()
    )
    db.delete(db_account)
    db.commit()
    return


def update_account(db: Session, account: Account):
    old_account_query = db.query(schema.Account).filter(schema.Account.id == account.id)
    old_account = old_account_query.first()
    if not old_account:
        return False

    # if user.accounts is an empty array, SQLAlechemy raises an error
    if len(account.transactions) == 0:
        del account.transactions

    old_account_query.update(account.dict())
    db.commit()
    db.refresh(old_account)
    return old_account
