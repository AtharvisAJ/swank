# db.py
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import *

# Determine the path to the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))

# Database URL (SQLite in this case)
DATABASE_URL = f"sqlite:///{os.path.join(backend_dir, 'test.db')}"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define your t-shirt model
Base = declarative_base()

class Tshirt(Base):
    __tablename__ = "tshirts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Integer)
    image_url = Column(String)  # Add an image URL field

# Create the database tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Insert dummy t-shirt data
def insert_dummy_data():
    db = SessionLocal()

    # Insert three dummy t-shirt entries
    dummy_tshirts = [
        Tshirt(title="T-shirt 1", price=20.99, image_url="tshirt1.jpg"),
        Tshirt(title="T-shirt 2", price=18.99, image_url="tshirt2.jpg"),
        Tshirt(title="T-shirt 3", price=22.99, image_url="tshirt3.jpg"),
    ]

    db.add_all(dummy_tshirts)
    db.commit()
    db.close()

if __name__ == "__main__":
    # Initialize the database and insert dummy data
    init_db()
    insert_dummy_data()
