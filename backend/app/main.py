from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import crud, models, schemas, database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
#     allow_headers=["*"],
    
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (modifique se necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

@app.patch("/users/{user_id}", response_model=dict)
def update_user(user_id: UUID, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    return crud.update_user(db, user_id, user)


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: UUID, db: Session = Depends(database.get_db)):
    return crud.delete_user(db,user_id)
  

# Address
@app.post("/address/", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(database.get_db)):
    return crud.create_address(db, address)

@app.get("/address/{user_id}", response_model=schemas.AddressResponse)
def read_address(user_id: UUID, db: Session = Depends(database.get_db)):
    return crud.get_address(db, user_id)
  
    
@app.patch("/address/{user_id}", response_model=dict)
def update_address(user_id: UUID, address: schemas.AddressUpdate, db: Session = Depends(database.get_db)):
    return crud.update_address(db,user_id, address)