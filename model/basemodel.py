from pydantic import BaseModel,EmailStr

class BlogSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str