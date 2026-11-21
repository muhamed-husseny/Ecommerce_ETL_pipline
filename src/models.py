from datetime import datetime
from xmlrpc.client import FastParser

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, PrimaryKeyConstraint, Nullable
from sqlalchemy.orm import DeclarativeBase
from unicodedata import category


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "dim_products"


    id = Column(Integer, primary_key=True, autoincrement=False)
    title= Column(String(200), nullable=False)
    category_slug = Column(String(100),nullable=False)
    price = Column(Float,nullable=False)
    rating = Column(Float, default=0.0)
    stock = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now())




class CategoryAnalytics(Base):
    __tablename__ = "category_analytics"

    category_slug = Column(String(100), primary_key=True)
    total_products = Column(Integer, nullable=False)
    avg_price = Column(Float, nullable=False)
    total_inventory_value = Column(Float, nullable=False)
    avg_rating = Column(Float, nullable=False)



class ETLLog(Base):
    __tablename__ = "etl_audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_timestamp = Column(DateTime, default=datetime.utcnow)
    records_fetched = Column(Integer, default=0)
    records_rejected = Column(Integer, default=0)
    records_loaded = Column(Integer, default=0)
    status = Column(String(50), nullable=False)




def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine



if __name__ == "__main__":
    DB_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/ecommerce_warehouse"
    init_db(DB_URL)
    print("Tables created successfully!")