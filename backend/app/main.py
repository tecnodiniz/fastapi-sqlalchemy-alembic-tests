from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import crud, models, schemas, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root():
    return {"message":"Api version 0.0.1","status": "ok"}


@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: UUID, db: Session = Depends(database.get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return user
    
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    users = crud.get_users(db)
    return users


# Address
@app.post("/addresses/", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(database.get_db)):
    return crud.create_address(db, address)

@app.get("/addressess/{address_id}", response_model=schemas.AddressResponse)
def read_address(address_id: UUID, db: Session = Depends(database.get_db)):
    address = crud.get_address(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")