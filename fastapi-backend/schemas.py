from pydantic import BaseModel
from datetime import date
import models


class StockAddRequest(BaseModel):
    symbol: str


class UpdateStockDaily(BaseModel):
    price: float
    ma50: float
    ma200: float
    forward_eps: float
    forward_pe: float
    dividend: float


class AddStockHistorical(BaseModel):
    stock_id: int
    closing_price: int
    date: date
