import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    profile: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class TweetsBase(BaseModel):
    user_id: int
    tweet: str


class TweetsCreate(TweetsBase):
    pass


class Tweets(TweetsBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserFollowListBase(BaseModel):
    user_id: int
    follow_user: int


class UserFollowListCreate(UserFollowListBase):
    pass


class UserFollowList(UserFollowListBase):
    created_at: datetime.datetime

    class Config:
        orm_mode = True


# class TweetModel(BaseModel):
#     id: int
#     tweet_str: str
#
#     class Config:
#         orm_mode = True
#
#
# class FollowModel(BaseModel):
#     id: int
#     follow: int
#
#     class Config:
#         orm_mode = True
#
#
# class UnFollowModel(BaseModel):
#     id: int
#     unfollow: int
#
#     class Config:
#         orm_mode = True
