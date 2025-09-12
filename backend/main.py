
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import hashlib


# یک مسیر برای فایل دیتایس تایین کردم
DB_FILE_PATH = "./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"


# ایجاد کردم SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# یک کلاس سشن ایجاد کردم
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# یک کلاس ایجاد کردم که مدلهارو تعریف کنم
Base = declarative_base()

# برای دیتابیس مدل یوزر رو تعریف کردم
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


#  برای درخواست ها و پاسخ ها تعریف کردمPydantic مدل
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True


app = FastAPI()



origins = [
        "http://localhost",

        "http://localhost:3000", 
        
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )



@app.on_event("startup")
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    print(f"Database file created at: {DB_FILE_PATH}") 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()



@app.post("/users/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="نام کاربری قبلاً استفاده شده .")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ایمیل قبلاً استفاده شده .")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)

    db.commit()
    db.refresh(db_user)
    return db_user



@app.get("/users/", response_model=List[UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="کاربر یافت نشد.")
    return user



@app.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="کاربر یافت نشد.")

    if user_update.username is not None and user_update.username != db_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="نام کاربری قبلاً استفاده شده است.")
        db_user.username = user_update.username

    if user_update.email is not None and user_update.email != db_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ایمیل قبلاً استفاده شده است.")
        db_user.email = user_update.email

    if user_update.password is not None:
        db_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="کاربر یافت نشد.")
    db.delete(db_user)
    db.commit()
    
    return {"message": "کاربر با موفقیت حذف شد."}
