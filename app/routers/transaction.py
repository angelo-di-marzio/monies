from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from controllers import transaction as transaction_controller
from model.transaction import Transaction, TransactionBase, Deposit
from services.database.init_db import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.get("/", response_model=list[Transaction])
async def get_transactions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return transaction_controller.get_all(db, skip, limit)


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return transaction_controller.get_one(db, transaction_id)


@router.post("/", response_model=Transaction, status_code=201)
async def create_transaction(
    transaction: TransactionBase, db: Session = Depends(get_db)
):
    return transaction_controller.create(db, transaction)


@router.post("/deposit", response_model=Transaction, status_code=201)
async def deposit_atm(body: Deposit, db: Session = Depends(get_db)):
    return transaction_controller.create_atm_transaction(
        db, body.amount, body.account_id
    )


@router.delete("/{transaction_id}", status_code=204)
async def delete_account(transaction_id: int, db: Session = Depends(get_db)):
    return transaction_controller.delete(db, transaction_id)


@router.put("/", response_model=Transaction)
async def update_transaction(transaction: Transaction, db: Session = Depends(get_db)):
    return transaction_controller.update(db, transaction)
