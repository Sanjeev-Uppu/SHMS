from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    full_name: str
    hospital_name: str
    email: EmailStr 
    phone_number: str
    password: str
    confirm_password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str