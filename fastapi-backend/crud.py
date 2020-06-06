from sqlalchemy.orm import Session

import models
import schemas


def get_stock_daily(db: Session, id: int):
    print("IDboop", id)
    # return db.query(models.Stock).all()
    return db.query(models.Stock).filter(models.Stock.id == id).first()


def get_stock_historical(db: Session, id: int):
    return db.query(models.HistoricalStock).filter(models.Stock.id == id).first()


def add_stock(db: Session, symbol: str):
    new_stock = models.Stock()
    new_stock.symbol = symbol
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


def add_stock_historical(db: Session, stock: models.Stock, symbol: str):
    return


def update_stock_daily(db: Session, stock: schemas.UpdateStockDaily):
    return


def delete_stock(db: Session, symbol: str):
    return
