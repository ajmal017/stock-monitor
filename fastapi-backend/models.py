from database.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship


class Stock(Base):
    """Summary for each stock's key metrics."""

    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))
    forward_pe = Column(Numeric(10, 2))
    forward_eps = Column(Numeric(10, 2))
    dividend_yield = Column(Numeric(10, 2))
    historical_data = relationship("HistoricalData", back_populates="stock")


class HistoricalData(Base):
    """Historical stock data, a many to one relationship with Stock. 
    Each Stock has multiple HistoricalData objects."""

    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    closing_price = Column(Numeric(10, 2))
    date = Column(DateTime)
    stock = relationship("Stock", back_populates="historical_data")
