#!/usr/bin/env python3
from sqlalchemy.orm import Session
from model.transaction import TransactionBase
from services.database.transaction import (
    get_last_transaction,
    get_transaction,
)
from services.database.account import get_account


def validate_account_id(db: Session, account_id: int):
    origin_account = get_account(db, account_id)
    if not origin_account:
        return False
    return True


def validate_external_account_id(db: Session, external_account_id: int):
    external_account = get_account(db, external_account_id)
    if not external_account:
        return False
    return True


def validate_balance(db: Session, transaction: TransactionBase):
    last_transaction = get_last_transaction(db, transaction.account_id)

    if not last_transaction:
        return False
    if transaction.account_id == last_transaction.account_id:
        if transaction.amount > last_transaction.account_balance:
            return False
    elif transaction.account_id == last_transaction.external_account_id:
        if transaction.amount > last_transaction.external_account_balance:
            return False
    return True


def process_balance(db: Session, transaction_amount: int, account_id: int, type: str):
    previous_balance = get_balance(db, account_id)
    if type == "debit":
        balance = previous_balance - transaction_amount
    elif type == "credit":
        balance = previous_balance + transaction_amount
    return balance


def get_balance(db: Session, account_id: int):
    last_transaction = get_last_transaction(db, account_id)
    if not last_transaction:
        return 0
    if last_transaction and last_transaction.account_id == account_id:
        return last_transaction.account_balance
    elif last_transaction and last_transaction.external_account_id == account_id:
        return last_transaction.external_account_balance
