from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import logging
from database import engine, Base
from controllers import (
    user_router,
    product_router
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s %(levelname)s - %(message)s'
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POS API",
    description="API สำหรับระบบ POS ร้านอาหาร",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/uploads',StaticFiles(directory='uploads'), name='uploads')

app.include_router(user_router)
app.include_router(product_router)

@app.get('/')
def root():
    return {'message': 'Hello API Server Running by kob'}

