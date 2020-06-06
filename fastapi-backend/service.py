import yfinance

from sqlalchemy.orm import Session

import crud
import schemas
import models


def fetch_daily_data(id: int, db: Session):
    """Fetches daily and historical data for stock symbol and populates the database when finished."""
    old_stock_entry = crud.get_stock_daily(db, id)
    data = yfinance.Ticker(old_stock_entry.symbol)

    new_daily = data.info

    updated_stock_daily = schemas.UpdateStockDaily(
        price=new_daily["previousClose"],
        ma50=new_daily["fiftyDayAverage"],
        ma200=new_daily["twoHundredDayAverage"],
        forward_eps=new_daily["forwardEps"],
        forward_pe=new_daily["forwardPE"],
        dividend=new_daily["dividendYield"]
    )
    crud.update_stock_daily(db, updated_stock_daily)


def fetch_historical_data(id: int, db: Session):
    stock = crud.get_stock_daily(db, id)
    data_summary = yfinance.Ticker(stock.symbol)
    historical = data_summary.history(period="max")
    return
