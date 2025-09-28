from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserResponse(UserBase):
    id: UUID
    role: str

    class Config:
        from_attributes = True  

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    role: str | None = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
