from sqlalchemy.orm import Session

import models
import schemas


def get_stock(id: int, db: Session):
    return db.query(models.Stock).filter(models.Stock.id == id).first()


def get_stock_with_symbol(symbol: str, db: Session):
    return db.query(models.Stock).filter(models.Stock.symbol == symbol).first()


def get_all_stocks(db: Session):
    return db.query(models.Stock).all()


def get_historical_data(id: int, db: Session):
    return db.query(models.HistoricalData).filter(models.HistoricalData.stock_id == id).all()


def add_stock(symbol: str, db: Session):
    new_stock = models.Stock()
    new_stock.symbol = symbol
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


def add_historical_data(data: schemas.AddHistoricalData, stock: models.Stock, db: Session):
    historical_entry = models.HistoricalData()
    historical_entry.stock_id = data.stock_id
    historical_entry.closing_price = data.closing_price
    historical_entry.date = data.date
    stock.historical_data.append(historical_entry)
    db.add(stock)
    db.add(historical_entry)
    db.commit()
    return


def update_stock(id: int, updated_data: schemas.UpdateStock, db: Session):
    current_data = get_stock(id, db)
    current_data.price = updated_data.price
    current_data.ma50 = updated_data.ma50
    current_data.ma200 = updated_data.ma200
    current_data.forward_eps = updated_data.forward_eps
    current_data.forward_pe = updated_data.forward_pe
    current_data.dividend_yield = updated_data.dividend_yield
    db.add(current_data)
    db.commit()
    db.refresh(current_data)
    return current_data


def delete_stock(id: int, db: Session):
    """Deletes historical data and stock summary."""
    stock = get_stock(id, db)
    for historical_data in stock.historical_data:
        db.delete(historical_data)
        db.commit()
    db.delete(stock)
    db.commit()
    return
