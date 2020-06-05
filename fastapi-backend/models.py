from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from database.session import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))
    forward_pe = Column(Numeric(10, 2))
    forward_eps = Column(Numeric(10, 2))
    dividend_yield = Column(Numeric(10, 2))
    historical_data = relationship("HistoricalStock", back_populates="stock")


class HistoricalStock(Base):
    __tablename__ = "historical_stocks"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    closing_price = Column(Numeric(10, 2))
    date = Column(DateTime)
    stock = relationship("Stock", back_populates="historical_data")
