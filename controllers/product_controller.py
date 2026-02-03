from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from database import get_db
from models.Product import Product

router = APIRouter(prefix='/api/products', tags=['products'])
 
UPLOAD_DIR = 'uploads'

@router.post('/')
def created_product(product: dict, db: Session = Depends(get_db)):
    try:
        db_product = Product(
            image='', 
            name=product['name'], 
            price=product['price']
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
