from sqlalchemy.orm import Session

import models
import schemas


def get_stock_daily(db: Session, stock_id: int):
    return


def get_stock_daily_symbol(db: Session, symbol: str):
    return


def get_stock_historical(db: Session, stock_id: int):
    return


def get_stock_historical_symbol(db: Session, symbol: str):
    return


def add_stock(db: Session, symbol: str):
    return


def remove_stock(db: Session, symbol: str):
    return
