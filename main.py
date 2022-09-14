from dataclasses import field
from uuid import UUID
from datetime import date
from typing import Optional
from datetime import datetime

#pydantic
from pydantic import BaseModel
from pydantic import EmailStr,Field

#fastApi
from fastapi import FastAPI

app= FastAPI()

#__________Users models__________________

class UserBase(BaseModel):
    userId:UUID = Field(...)
    email:EmailStr = Field(...)

class User(UserBase):
    
    firstname : str =  Field(
        ...,
        min_length=1,
        max_length=40
    )
    lastname : str =  Field(
        ...,
        min_length=1,
        max_length=40
    )
    birth_date: Optional[date] = Field(default=None)
    

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

#_________________twitter Models__________________________

class Twitt(BaseModel):
    twittId : UUID = Field(...)
    content : str = Field(
        ...,
        max_length=256,
        min_length=1)
    create_at : datetime = Field(default=datetime.now())
    update_at : Optional[datetime] = Field(default=None)
    by : User = Field(...)

@app.get(path="/")
def home():
    return {"twitter":"funcionando"}