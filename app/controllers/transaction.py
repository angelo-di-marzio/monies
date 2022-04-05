#!/usr/bin/env python3
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.transaction import Transaction, TransactionBase, TransactionCreate
from services.database.transaction import (
    create_transaction,
    get_transaction,
    get_transactions,
    update_transactions,
    delete_transactions,
)
from services.transaction import (
    validate_account_id,
    validate_external_account_id,
    validate_balance,
    get_balance,
    process_balance,
)


def create(db: Session, base_transaction: TransactionBase):
    if not validate_account_id(db, base_transaction.account_id):
        raise HTTPException(status_code=400, detail="Wrong account id !")

    if not validate_external_account_id(db, base_transaction.external_account_id):
        raise HTTPException(status_code=400, detail="Wrong external account id !")

    if not validate_balance(db, base_transaction):
        raise HTTPException(status_code=400, detail="Not enough money !")

    balance = process_balance(
        db, base_transaction.amount, base_transaction.account_id, "debit"
    )
    external_balance = process_balance(
        db, base_transaction.amount, base_transaction.external_account_id, "credit"
    )

    if not balance or not external_balance:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    logging.info("creating transaction")
    transaction = TransactionCreate(
        amount=base_transaction.amount,
        communication=base_transaction.communication,
        external_account_id=base_transaction.external_account_id,
        external_account_balance=external_balance,
        account_id=base_transaction.account_id,
        account_balance=balance,
    )
    return create_transaction(db, transaction)


def create_atm_transaction(db: Session, amount: int, account_id: int):

    if not validate_external_account_id(db, account_id):
        raise HTTPException(status_code=400, detail="Wrong external account id !")

    # get previous balance
    previous_balance = get_balance(db, account_id)
    if previous_balance:
        balance = previous_balance + amount
    else:
        balance = amount
    logging.info("creating deposit transaction")
    transaction = TransactionCreate(
        amount=amount,
        communication="ATM deposit",
        external_account_id=account_id,
        external_account_balance=balance,
        account_id=None,
        account_balance=None,
    )

    return create_transaction(db, transaction)


def get_account_balance(db: Session, account_id: int):
    if not validate_account_id(db, account_id):
        raise HTTPException(status_code=400, detail="Wrong account id !")
    balance = get_balance(db, account_id)
    return balance


def get_one(db: Session, transaction_id: int):
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Not found")
    return transaction


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return get_transactions(db, skip=skip, limit=limit)


def delete(db: Session, transaction_id: int):
    return delete_transactions(db, transaction_id)


def update(db: Session, transaction: Transaction):
    old_transaction = get_transaction(db, transaction.id)
    if not old_transaction:
        raise HTTPException(status_code=404, detail="Not found")
    new_transaction = update_transactions(db, transaction)
    return new_transaction
