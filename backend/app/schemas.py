from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional 


# Address
class AddressBase(BaseModel):
    user_id: UUID
    street: str
    city: str
    state: str
    zip_code: str

class AddressUpdate(BaseModel):
    street:  Optional[str]  = None
    city:    Optional[str] = None
    state:   Optional[str] = None
    zip_code:Optional[str]  = None

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase): 
    id: UUID
    user_id: UUID
    
    class Config:
        from_attributes = True

# User
class UserBase(BaseModel):
    name: Optional[str]
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    address: Optional["AddressResponse"]
    
    class Config:
        from_attributes = True





        


