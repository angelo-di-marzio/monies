from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from controllers import account as account_controller
from controllers import transaction as transaction_controller
from model.account import Account, AccountBase
from services.database.init_db import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.get("/", response_model=list[Account])
async def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return account_controller.get_all(db, skip, limit)


@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    return account_controller.get_one(db, account_id)


@router.get("/{account_id}/balance", response_model=int)
async def get_account_balance(account_id: int, db: Session = Depends(get_db)):
    return transaction_controller.get_account_balance(db, account_id)


@router.post("/", response_model=Account, status_code=201)
async def create_account(account: AccountBase, db: Session = Depends(get_db)):
    return account_controller.create(db, account)


@router.delete("/{account_id}", status_code=204)
async def delete_account(account_id: int, db: Session = Depends(get_db)):
    return account_controller.delete(db, account_id)


@router.put("/", response_model=Account)
async def update_account(account: Account, db: Session = Depends(get_db)):
    return account_controller.update(db, account)
