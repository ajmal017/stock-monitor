import time

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.session import SessionLocal, engine
from sqlalchemy.orm import Session

import crud
import models
import schemas
import service

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/stocks")
async def add_stock(add_stock_request: schemas.StockAddRequest, db: Session = Depends(get_db)):
    new_stock = crud.add_stock(db, add_stock_request.symbol)
    new_stock_id = new_stock.id
    service.fetch_daily_data(new_stock_id, db)
    return {"status": "success"}


@app.delete("/stocks/{id}")
def delete_stock(id: int, db: Session = Depends(get_db)):
    clean_symbol = clean_string(symbol)
    crud.delete_stock(db, clean_symbol)
    return {"status": "success"}


@app.get("/stocks/{id}/daily")
def get_stock_daily(id: int, db: Session = Depends(get_db)):
    """Get all stocks daily data."""
    clean_symbol = clean_string(symbol)
    crud.get_stock_daily(db, clean_symbol)
    return {"status": "success"}


@app.get("/stocks/{symbol}/historical")
def get_stock_historical(symbol: str, db: Session = Depends(get_db)):
    clean_symbol = clean_string(symbol)
    crud.get_stock_historical(db, clean_symbol)
    return {"status": "success"}


@app.get("/")
def read_root(request: Request):
    current_time = time.time()

    return templates.TemplateResponse("index.html", {"request": request, "time": current_time})


@app.get("/time")
def read_time():
    current_time = time.time()
    return {"time": current_time}


def clean_string(data: str):
    return data.strip().upper()
