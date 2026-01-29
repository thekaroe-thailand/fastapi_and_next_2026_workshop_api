from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import logging

from database import get_db
from models.User import User
from libs.auth import (
    get_password_hash
)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register")
def register(user: dict, db: Session = Depends(get_db)):
    try: 
        db_user = db.query(User).filter(
            (User.email == user["email"]) | (User.username == user["username"])
        ).first()

        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username or email exists"
            )
        
        hashed_password = get_password_hash(user["password"])
        
        user = User(
            email=user["email"],
            username=user["username"],
            full_name=user["full_name"],
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )