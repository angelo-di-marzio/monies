#!/usr/bin/env python3
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    DateTime,
    Sequence,
)
from sqlalchemy.orm import relationship
from services.database.init_db import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    address = Column(String)
    coordinates = Column(String)

    accounts = relationship("Account", back_populates="owner")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    number = Column(Integer, Sequence("account_number"))
    devise = Column(String)
    creation_datetime = Column(DateTime, default=datetime.datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, Sequence("transaction_number"))
    creation_datetime = Column(DateTime, default=datetime.datetime.utcnow)
    amount = Column(Integer)
    communication = Column(String)

    # account_previous_balance = Column(String)
    account_balance = Column(Integer)

    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="transactions")

    external_account_id = Column(Integer)

    external_account_balance = Column(Integer)
