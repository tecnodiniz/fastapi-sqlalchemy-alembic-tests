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

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: UUID
    user_id: UUID
    
    class Config:
        orm_mode = True

# User
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID
    address: Optional["AddressResponse"]
    
    class Config:
        orm_mode = True





        


