import time
import json

from database.session import SessionLocal, engine
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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


@ app.get("/")
def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@ app.get("/stocks")
def get_all_stocks(db: Session = Depends(get_db)):
    return crud.get_all_stocks(db)


@ app.get("/stocks/{id}")
def get_stock_daily(id: int, db: Session = Depends(get_db)):
    """Get all stocks daily data."""
    return crud.get_stock(id, db)


@ app.get("/stocks/{id}/historical")
def get_stock_historical(id: int, db: Session = Depends(get_db)):
    return service.get_historical_data(id, db)


@app.post("/stocks")
async def add_stock(add_stock_request: schemas.AddStock, background_tasks: BackgroundTasks,
                    db: Session = Depends(get_db)):

    new_stock = crud.add_stock(add_stock_request.symbol.strip().upper(), db)

    service.fetch_daily_data(new_stock.id, db)
    background_tasks.add_task(service.fetch_historical_data, new_stock.id, db)

    return {"status": "success"}


@ app.delete("/stocks/{id}")
def delete_stock(id: int, db: Session = Depends(get_db)):
    """Removes historical data and stock summary."""
    crud.delete_stock(id, db)
    return {"status": "success"}
