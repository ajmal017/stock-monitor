from pydantic import BaseModel


class AddStockRequest(BaseModel):
    symbol: str
