#!/usr/bin/env python3
from fastapi import FastAPI
from routers.user import router as user_rooter

from routers.account import router as account_rooter
from routers.transaction import router as transaction_rooter


app = FastAPI()

app.include_router(transaction_rooter)
app.include_router(account_rooter)
app.include_router(user_rooter)
