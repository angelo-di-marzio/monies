from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from controllers import user as user_controller
from model.user import User, UserBase
from services.database.init_db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_controller.get_all(db, skip, limit)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_one(db, user_id)


@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    return user_controller.create(db, user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.delete(db, user_id)


@router.put("/", response_model=User)
async def update_user(user: User, db: Session = Depends(get_db)):
    return user_controller.update(db, user)
