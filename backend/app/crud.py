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
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
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

    # Se o e-mail foi enviado na atualização, verifica se já está cadastrado para outro usuário
    if "email" in update_data:
        email_exists = db.query(models.User).filter(
            models.User.email == update_data["email"],
            models.User.id != user_id  # Garante que não estamos verificando o próprio usuário
        ).first()

        if email_exists:
            raise HTTPException(status_code=400, detail="Este e-mail já está em uso por outro usuário")

    # Se o usuário quer atualizar a senha, hash da nova senha
    if "password" in update_data:
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

    try:
        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return {"mensagem": "Usuário atualizado"}  # Retorna o usuário atualizado

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

def get_address(db: Session, address_id: UUID):
    return db.query(models.Address).filter(models.Address.id == address_id).join(models.Address.user).first()
