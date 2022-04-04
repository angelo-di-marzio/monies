#!/usr/bin/env python3
from sqlalchemy import or_
from sqlalchemy.orm import Session
from model.transaction import Transaction
from . import schema


def create_transaction(db: Session, transaction: Transaction):
    db_transaction = schema.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transaction(db: Session, transaction_id: int):
    return (
        db.query(schema.Transaction)
        .filter(schema.Transaction.id == transaction_id)
        .first()
    )


def get_last_transaction(db: Session, account_id: int):
    return (
        db.query(schema.Transaction)
        .filter(
            or_(
                schema.Transaction.account_id == account_id,
                schema.Transaction.external_account_id == account_id,
            )
        )
        .order_by(schema.Transaction.creation_datetime.desc())
        .first()
    )


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schema.Transaction).offset(skip).limit(limit).all()


def delete_transactions(db: Session, account_id: int):
    db_transaction = (
        db.query(schema.Transaction).filter(schema.Transaction.id == account_id).first()
    )
    db.delete(db_transaction)
    db.commit()
    return


def update_transactions(db: Session, transaction: Transaction):
    old_transaction_query = db.query(schema.Transaction).filter(
        schema.Transaction.id == transaction.id
    )
    old_transaction = old_transaction_query.first()
    if not old_transaction:
        return False
    old_transaction_query.update(transaction.dict())
    db.commit()
    db.refresh(old_transaction)
    return old_transaction
