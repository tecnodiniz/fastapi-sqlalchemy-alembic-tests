from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()


# Address

def create_address(db: Session, address: schemas.AddressCreate):

    db_address = models.Address(
        user_id = address.user_id,
        street = address.street,
        city = address.city,
        state = address.state,
        zip_code = address.zip_code
    )

    try:
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        
        return db_address
    except Exception as e:
        db.rollback()  # Rollback em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao criar endereço: {str(e)}")

def get_address(db: Session, address_id: UUID):
    return db.query(models.Address).filter(models.Address.id == address_id).join(models.Address.user).first()
