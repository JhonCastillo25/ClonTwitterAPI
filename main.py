from dataclasses import field
from uuid import UUID
from datetime import date
from typing import Optional,List
from datetime import datetime

#pydantic
from pydantic import BaseModel
from pydantic import EmailStr,Field

#fastApi
from fastapi import FastAPI
from fastapi import status

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

class Tweet(BaseModel):
    tweetId : UUID = Field(...)
    content : str = Field(
        ...,
        max_length=256,
        min_length=1)
    create_at : datetime = Field(default=datetime.now())
    update_at : Optional[datetime] = Field(default=None)
    by : User = Field(...)


#______________________Path Operations__________________________

##___Users

### sign-up user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["User"]
)
def signup():
    pass

### login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["User"]
)
def login():
    pass

### show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["User"]
)
def show_all_users():
    pass

### show a user
@app.get(
    path="/users/{userId}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["User"]
)
def show_a_user():
    pass

### delete a user
@app.delete(
    path="/users/{userId}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["User"]
)
def delete_user():
    pass

### update a user
@app.put(
    path="/users/{userId}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["User"]
)
def update_user():
    pass


##___Tweets

### Home with all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    return {"twitter":"funcionando"}

###post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post_tweet():
    pass

###show a tweet
@app.get(
    path="/tweets/{tweetId}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_tweet():
    pass

### delete a tweet
@app.delete(
    path="/tweets/{tweetId}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_tweet():
    pass

### update a tweet
@app.put(
    path="/tweets/{tweetId}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_tweet():
    pass