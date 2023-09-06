from fastapi import *
from sqlalchemy.orm import Session
from models import Tshirt  # Import the Tshirt model from the models module
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from pydantic import *  # Import Pydantic
from typing import List


# Configure CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database URL (creates a local database file)
DATABASE_URL = "sqlite:///./test.db"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

TshirtResponseModel = create_model(
    "TshirtResponse",
    id=(int, ...),
    title=(str, ...),
    price=(float, ...),
    image_url=(str, ...),
)

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

Base.metadata.create_all(bind=engine)

# Pydantic models
class TshirtBase(BaseModel):
    title: str
    price: int
    image_url: str

class TshirtCreate(TshirtBase):
    pass

class TshirtResponse(TshirtBase):
    id: int

@app.get("/")
def read_root():
    return {"message": "Welcome to Swankitt API!"}

@app.post("/tshirts/", response_model=TshirtResponse)  # Use the Pydantic model as response_model
def create_tshirt(tshirt: TshirtCreate):
    db = SessionLocal()
    db_tshirt = Tshirt(**tshirt.dict())  # Create a Tshirt instance from the Pydantic model
    db.add(db_tshirt)
    db.commit()
    db.refresh(db_tshirt)
    db.close()
    return db_tshirt



# Create a Pydantic model for a list of Tshirts
class TshirtsList(BaseModel):
    tshirts: List[Tshirt]
    class Config:
        arbitrary_types_allowed = True

# Update your route like this
@app.get("/tshirts/", response_model=list[TshirtResponseModel])
def read_tshirts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a list of t-shirts with pagination.
    """
    tshirts = db.query(Tshirt).offset(skip).limit(limit).all()
    return tshirts

@app.get("/tshirts/{tshirt_id}", response_model=TshirtResponse)  # Use the Pydantic model as response_model
def read_tshirt(tshirt_id: int):
    db = SessionLocal()
    tshirt = db.query(Tshirt).filter(Tshirt.id == tshirt_id).first()
    db.close()
    if tshirt is None:
        raise HTTPException(status_code=404, detail="T-shirt not found")
    return tshirt

@app.get("/tshirts/images/{tshirt_id}")
def get_tshirt_image(tshirt_id: int):
    db = SessionLocal()
    tshirt = db.query(Tshirt).filter(Tshirt.id == tshirt_id).first()
    db.close()
    if not tshirt or not tshirt.image_url:
        raise HTTPException(status_code=404, detail="T-shirt not found or image not available")
    return FileResponse(tshirt.image_url)
