#!/usr/bin/env python3
from datetime import date
from typing import Optional
from pydantic import BaseModel
from model.account import Account

# User without id to be used for user creation
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birth_date: date
    address: str


# Full user
class User(UserBase):
    id: int
    coordinates: Optional[str] = None
    accounts: list[Account] = []

    class Config:
        orm_mode = True
