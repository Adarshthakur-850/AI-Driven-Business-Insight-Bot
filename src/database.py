import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, timedelta
import random

Base = declarative_base()

# --- Database Models ---
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    segment = Column(String)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    date = Column(Date)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    total_amount = Column(Float)
    
    customer = relationship("Customer")
    product = relationship("Product")

# --- Database Setup ---
DB_URL = "sqlite:///./business_data.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Sample Data Generation ---
def generate_sample_data():
    """Generates sample data if DB is empty."""
    db = SessionLocal()
    
    if db.query(Customer).count() > 0:
        db.close()
        return

    print("Generating sample data...")
    
    # Customers
    countries = ['USA', 'UK', 'Germany', 'France', 'India', 'Canada']
    segments = ['Consumer', 'Corporate', 'Home Office']
    customers = []
    for i in range(50):
        c = Customer(
            name=f"Customer_{i}",
            country=random.choice(countries),
            segment=random.choice(segments)
        )
        customers.append(c)
    db.add_all(customers)
    db.commit()

    # Products
    categories = ['Electronics', 'Furniture', 'Clothing', 'Office Supplies']
    products = []
    for i in range(20):
        p = Product(
            name=f"Product_{i}",
            category=random.choice(categories),
            price=round(random.uniform(10, 500), 2)
        )
        products.append(p)
    db.add_all(products)
    db.commit()

    # Orders
    orders = []
    start_date = datetime.now() - timedelta(days=365)
    customer_ids = [c.customer_id for c in db.query(Customer).all()]
    product_objs = db.query(Product).all()
    
    for i in range(500):
        p = random.choice(product_objs)
        qty = random.randint(1, 5)
        o = Order(
            date=(start_date + timedelta(days=random.randint(0, 365))).date(),
            customer_id=random.choice(customer_ids),
            product_id=p.product_id,
            quantity=qty,
            total_amount=round(p.price * qty, 2)
        )
        orders.append(o)
    
    db.add_all(orders)
    db.commit()
    db.close()
    print("Sample data generated successfully.")

if __name__ == "__main__":
    init_db()
    generate_sample_data()
