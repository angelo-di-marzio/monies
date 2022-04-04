#!/usr/bin/env python3
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TransactionBase(BaseModel):
    amount: int
    communication: str
    account_id: Optional[int]
    external_account_id: int


class TransactionCreate(TransactionBase):
    account_balance: Optional[int]
    external_account_balance: int


class Transaction(TransactionCreate):
    id: int
    number: int
    creation_datetime: datetime

    class Config:
        orm_mode = True


class Deposit(BaseModel):
    amount: int
    account_id: int
