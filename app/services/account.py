#!/usr/bin/env python3
from sqlalchemy.orm import Session
from model.account import Account, AccountBase
from services.database.account import get_account
from services.database.user import get_user


def validate_user_id(db: Session, account: AccountBase):
    user = get_user(db, account.owner_id)
    if not user:
        return False
    return True


def validate_account_id(db: Session, account: AccountBase):
    account = get_account(db, account.owner_id)
    if not account:
        return False
    return True
