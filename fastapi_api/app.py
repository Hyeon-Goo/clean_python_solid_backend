import crud
import models
import schema
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app(test_config=None):
    app = FastAPI()

    @app.get("/ping")
    async def pong():
        return "pong"

    @app.post("/sign-up", response_model=schema.User)
    async def sign_up(sign_up_body: schema.UserCreate, db: Session = Depends(get_db)):
        db_user = crud.get_user_by_name(db, user_name=sign_up_body.name)
        if db_user:
            raise HTTPException(status_code=400, detail="Name already registerd")
        return crud.insert_user(db=db, user=sign_up_body)

    @app.post("/tweet", response_model=schema.Tweets)
    async def tweet(tweet_body: schema.TweetsCreate, db: Session = Depends(get_db)):
        user_id = tweet_body.user_id
        tweet_str = tweet_body.tweet
        db_user = crud.get_user(db, user_id)
        if not db_user:
            raise HTTPException(status_code=400, detail="User is not exist")
        if len(tweet_str) > 300:
            raise HTTPException(status_code=400, detail="Exceed tweet length lint.")
        return crud.insert_tweet(db, user_tweet=tweet_body)

    @app.post("/follow", response_model=schema.UserFollowList)
    async def follow(follow_body: schema.UserFollowListCreate, db: Session = Depends(get_db)):
        user_id = follow_body.user_id
        follow_user_id = follow_body.follow_user
        target_user = crud.get_user(db, user_id)
        follow_user = crud.get_user(db, follow_user_id)
        if not target_user or not follow_user:
            raise HTTPException(status_code=400, detail="User is not exist")
        return crud.insert_follow(db, follow_body)

    @app.post("/unfollow")
    async def unfollow(follow_body: schema.UserFollowListCreate, db: Session = Depends(get_db)):
        user_id = follow_body.user_id
        follow_user_id = follow_body.follow_user
        target_user = crud.get_user(db, user_id)
        follow_user = crud.get_user(db, follow_user_id)
        if not target_user or not follow_user:
            raise HTTPException(status_code=400, detail="User is not exist")
        return crud.insert_unfollow(db, follow_body)

    @app.get('/timeline/{user_id}')
    async def timeline(user_id: int, db:Session = Depends(get_db)):
        db_user = crud.get_user(db, user_id)
        if not db_user:
            raise HTTPException(status_code=400, detail="User is not exist")
        return crud.get_timeline(db, user_id)
# execute command in windows
# uvicorn main:app --reload
