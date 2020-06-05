import time
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.session import SessionLocal, engine
from sqlalchemy.orm import Session
import crud
import models
import schemas


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


@app.post("/stock")
def add_stock(stock: schemas.AddStockRequest, db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def read_root(request: Request):
    current_time = time.time()

    return templates.TemplateResponse("index.html", {"request": request, "time": current_time})


@app.get("/time")
def read_time():
    current_time = time.time()
    return {"time": current_time}
