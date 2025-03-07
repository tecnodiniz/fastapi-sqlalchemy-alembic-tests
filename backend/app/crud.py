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
    db_user = models.User(name=user.name, username=user.username, email=user.email, hashed_password=password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        db_address = models.Address(
        user_id = db_user.id,
        street = user.address.street,
        city =      user.address.city,
        state =     user.address.state,
        zip_code =  user.address.zip_code
    )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)

        return db_user
    
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        elif "username" in str(e.orig):
            raise HTTPException(status_code=400, detail="Username já cadastrado")
        else:
            raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário")
    
def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def update_user(db: Session, user_id: UUID, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Converte os dados enviados, excluindo valores não definidos
    update_data = user.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_exists = db.query(models.User).filter(
            models.User.email == update_data["email"],
            models.User.id != user_id  # Garante que não estamos verificando o próprio usuário
        ).first()

        if email_exists:
            raise HTTPException(status_code=400, detail="Este e-mail já está em uso por outro usuário")


    if "password" in update_data:
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

    try:
        if "address" in update_data:
            if isinstance(update_data["address"], dict):
                 if db_user.address:
                    for addr_key, addr_value in update_data["address"].items():
                        setattr(db_user.address, addr_key, addr_value)
                 else:
                    new_address = models.Address(**update_data["address"], user_id=user_id)
                    db.add(new_address)

        for key, value in update_data.items():
            if key != "address" and value is not None:
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        
        return {"mensagem": "Usuário atualizado"} 

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade. Verifique os dados enviados.")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar usuário: {str(e)}")


def delete_user(db: Session, user_id: UUID):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontral")
    
    try:
        db.delete(user)
        db.commit()

        return {"messagem": "Usuário deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário {e}") 

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

def get_address(db: Session, user_id: UUID):
      address = db.query(models.Address).filter(models.Address.user_id == user_id).first()
     
      if not address:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
      return address
 

def update_address(db: Session, user_id: UUID, address: schemas.AddressUpdate):
    db_address = db.query(models.Address).filter(models.Address.user_id == user_id).first()

    if not db_address:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    
    update_address = address.model_dump(exclude_unset=True)

    for key, value in update_address.items():
        setattr(db_address, key, value)

    try:
        db.commit()
        db.refresh(db_address)
        
        return {"mesagem": "Endereço atualizado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar endereço {e}")