from pydantic import BaseModel
from datetime import date
import models


class AddStock(BaseModel):
    symbol: str


class UpdateStock(BaseModel):
    price: float
    ma50: float
    ma200: float
    forward_eps: float
    forward_pe: float
    dividend_yield: float


class AddHistoricalData(BaseModel):
    stock_id: int
    closing_price: int
    date: date
