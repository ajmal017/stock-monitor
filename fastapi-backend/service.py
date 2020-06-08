from datetime import date
from enum import Enum

from sqlalchemy.orm import Session
import pandas as pd
import yfinance

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


class HistoricalDataType(Enum):
    DAILY = 1
    MA200 = 2
    MA50 = 3


class HistoricalData():
    def __init__(self, data: list, data_type: HistoricalDataType):
        self.data = data
        self.data_type: data_type


def get_historical_data(id: int, db: Session):
    """format for nivo api. Returns a list of objects, historical time data of 50 moving"""
    data = crud.get_historical_data(id, db)

    daily = [{data[i].date: data[i].closing_price}
             for i in range(200, len(data))]
    ma50 = get_moving_average(data, 50, 200)
    ma200 = get_moving_average(data, 200, 200)

    return [
        HistoricalData(daily, HistoricalDataType.DAILY),
        HistoricalData(ma50, HistoricalDataType.MA50),
        HistoricalData(ma200, HistoricalDataType.MA200)
    ]


def get_moving_average(data: list, num_days: int, start_offset: int):
    """Returns a HistoricalData object. Data is a list of dictionaries
    that each correspond with a stock price on a given date. start_offset dictates
    which entry the moving average should be first calculated. """
    moving_average = []
    for end in range(start_offset, len(data)):
        total = 0
        for start in range(end-num_days+1, end):
            total += data[start].closing_price
        moving_average.append({
            data[end].date: total / num_days
        })
    return moving_average
