import yfinance
from datetime import date
import pandas as pd
from sqlalchemy.orm import Session

import crud
import schemas
import models


def fetch_daily_data(id: int, db: Session):
    """Fetches daily data for stock symbol and populates the database when finished."""
    current_entry = crud.get_stock(id, db)
    data = yfinance.Ticker(current_entry.symbol)

    new_daily = data.info

    updated_stock = schemas.UpdateStock(
        price=new_daily["previousClose"],
        ma50=new_daily["fiftyDayAverage"],
        ma200=new_daily["twoHundredDayAverage"],
        forward_eps=new_daily["forwardEps"],
        forward_pe=new_daily["forwardPE"],
        dividend_yield=new_daily["dividendYield"]
    )
    crud.update_stock(id, updated_stock, db)


def fetch_historical_data(id: int, db: Session):
    """Fetches last 600 days of historical data for a given stock and populates the database when finished."""

    stock = crud.get_stock(id, db)
    data_summary = yfinance.Ticker(stock.symbol)
    historical = data_summary.history(period="max")
    for time_stamp, price in pd.Series(historical["Close"]).tail(600).items():
        historical_data = schemas.AddHistoricalData(
            stock_id=id,
            closing_price=price,
            date=time_stamp
        )
        crud.add_historical_data(historical_data, stock, db)
    return
