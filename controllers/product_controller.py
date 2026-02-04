from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
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

@router.post('/upload/{product_id}')
async def upload(product_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
    
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp"}
        # kob.jpg => .jpg
        file_ext = image.filename.split('.').pop().lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="file type not allowed"
            )
        
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        if product.image and os.path.exists(product.image):
            try:
                os.remove(product.image)
            except:
                pass
        
        product.image = f'/uploads/{filename}'
        db.commit()
        db.refresh(product)

        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get('/')
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product not found"
            )
        
        if product.image and os.path.exists(product.image.lstrip('/')):
            try:
                os.remove(product.image.lstrip('/'))
            except:
                pass
        
        db.delete(product)
        db.commit()

        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.put('/{product_id}')
def update_product(product_id: int, update_product: dict, db: Session = Depends(get_db)):
    try: 
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='product not found'
            )
        
        product.name = update_product['name']
        product.price = update_product['price']
        db.commit()
        db.refresh(product)

        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )