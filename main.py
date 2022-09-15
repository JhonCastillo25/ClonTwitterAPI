from dataclasses import field
from http.client import HTTPException
from pickle import TRUE
from unittest import result
from uuid import UUID
from datetime import date
from typing import Optional,List
from datetime import datetime
import json

#pydantic
from pydantic import BaseModel
from pydantic import EmailStr,Field

#fastApi
from fastapi import FastAPI
from fastapi import status,HTTPException
from fastapi import Body,Path,Query,Form

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

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8
    )    

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

#____________functions_______________



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
def signup(user:UserRegister = Body(...)):
    """
    Sign up user

    This path operation register a user in the app

    Parameters:
        - Request body parameter 
            - user : UserRegister
    
    Returns a json with the basic user information
        - userId : UUID
        - email : EmailStr
        - firstname : str
        - last name : str
        - birth date : date
    """
    with open("users.json","r+", encoding="utf-8") as f:  #leer archivo
        results = json.loads(f.read())     #caragar en formato json
        user_dict = user.dict()   #convertir clase a diccionario
        user_dict["userId"] = str(user_dict["userId"]) #cambiar atributos a str
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results)) #escribir usuario en el archivo
        return user

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
    """
    Show the all users

    this path operation shows the all users in the app

    Parameters:
        - 
    Return a json list with the all users in the app
        - userId : UUID
        - email : EmailStr
        - firstname : str
        - last name : str
        - birth date : date
    """
    with open ("users.json","r",encoding="utf-8") as f:
        results=json.loads(f.read())
        return results


### show a user
@app.get(
    path="/users/{userId}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["User"]
)
def show_a_user(
    userId: UUID = Path(...),
    ):
    """
    Show a one user

    this path operation shows the one users in the app for id

    Parameters:
        userId
    Return a json list with the all users in the app
        - userId : UUID
        - email : EmailStr
        - firstname : str
        - last name : str
        - birth date : date
    """
    with open("users.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(userId)
        for data in results:
            if  data["userId"] == id:
                return data
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")



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
    """
    Show the all tweets

    this path operation shows the all tweets in the app

    Parameters:
        - 
    Returns a json with the basic tweet information
        - tweetId : UUID
        - content : str
        - create_at : datetime 
        - update_at 
        - by : User  
    """
    with open ("tweets.json","r",encoding="utf-8") as f:
        results=json.loads(f.read())
        return results


###post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post_tweet(tweet:Tweet = Body(...)):
    """
    Post a tweet

    This path operation register a tweet in the app

    Parameters:
        - Request body parameter 
            - tweet : Tweet
    
    Returns a json with the basic tweet information
        - tweetId : UUID
        - content : str
        - create_at : datetime 
        - update_at 
        - by : User 
    """
    with open("tweets.json","r+", encoding="utf-8") as f:  #leer archivo
        results = json.loads(f.read())     #caragar en formato json
        tweets_dict = tweet.dict()   #convertir clase a diccionario
        tweets_dict["tweetId"] = str(tweets_dict["tweetId"]) #cambiar atributos a str
        tweets_dict["create_at"] = str(tweets_dict["create_at"])
        tweets_dict["update_at"] = str(tweets_dict["update_at"])
        tweets_dict["by"]["userId"] = str(tweets_dict["by"]["userId"])
        tweets_dict["by"]["birth_date"] = str(tweets_dict["by"]["birth_date"])
        results.append(tweets_dict)
        f.seek(0)
        f.write(json.dumps(results)) #escribir usuario en el archivo
        return tweet

###show a tweet
@app.get(
    path="/tweets/{tweetId}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_tweet(tweetId:UUID = Path(...)):
    """
    Show a one tweet by id

    this path operation shows the one tweet in the app by id

    Parameters:
        tweetId:UUID
    Returns a json with the basic tweet information
        - tweetId : UUID
        - content : str
        - create_at : datetime 
        - update_at 
        - by : User 
    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweetId)
        for data in results:
            if  data["tweetId"] == id:
                return data
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tweet not found")


### delete a tweet
@app.delete(
    path="/tweets/{tweetId}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_tweet(tweetId:UUID = Path(...)):
    """
    Delete a one tweet by id

    this path operation delete the one tweet in the app by id

    Parameters:
        tweetId:UUID
    Returns a json with the basic tweet information
        - tweetId : UUID
        - content : str
        - create_at : datetime 
        - update_at 
        - by : User 
    """
    with open("tweets.json","r+",encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweetId)
        for data in results:
            if  data["tweetId"] == id:
                
                results.remove(data)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return data
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tweet not found")

### update a tweet
@app.put(
    path="/tweets/{tweetId}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_tweet(
    tweetId:UUID = Path(...),
    content: str = Form(
        ..., 
        min_length=1,
        max_length=256)):
    """
    Update a one tweet by id

    this path operation update the one tweet in the app by id

    Parameters:
        tweetId:UUID
        content
    Returns a json with the basic tweet information
        - tweetId : UUID
        - content : str
        - create_at : datetime 
        - update_at 
        - by : User 
    """
    with open("tweets.json","r+",encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweetId)
        for data in results:
            if  data["tweetId"] == id:
                data['content'] = content
                data['updated_at'] = str(datetime.now())
                
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return data
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tweet not found")

    


