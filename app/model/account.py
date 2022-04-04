#!/usr/bin/env python3
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from model.transaction import Transaction
from enum import Enum


class Devise(str, Enum):
    usd = "USD"
    eur = "EUR"
    yuan = "YUAN"


class AccountBase(BaseModel):
    name: Optional[str] = None
    devise: Optional[Devise] = Devise.usd
    owner_id: Optional[int]


class Account(AccountBase):
    id: int
    number: int
    creation_datetime: datetime
    transactions: list[Transaction] = []

    class Config:
        orm_mode = True
