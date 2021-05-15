import crud
import models
import schema
import jwt
import bcrypt
import datetime
from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
    origins = [
        "http://localhost:8080"
        "http://localhost:8080/"
    ]
    app = FastAPI()
    oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.jwt_secret_key = "##!@ssddd###xc!!"

    def decode_token(token):
        return schema.User()

    @app.get("/ping")
    async def pong():
        return "pong"

    @app.post("/sign-up", response_model=schema.User)
    async def sign_up(sign_up_body: schema.UserCreate, db: Session = Depends(get_db)):
        db_user = crud.get_user_by_name(db, user_name=sign_up_body.name)
        if db_user:
            raise HTTPException(status_code=400, detail="Name already registered")
        return crud.insert_user(db=db, user=sign_up_body)

    @app.post("/login")
    async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        email = form_data.username
        db_user = crud.get_user_by_email(db, email)
        if not db_user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        row = db_user.hashed_password
        password = form_data.password

        if not row:
            raise HTTPException(status_code=400, detail="Invalid Approach")

        if not bcrypt.checkpw(password.encode('UTF-8'), row['hashed_password'].encode('UTF-8')):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        payload = {
            'user_id': db_user.user_id,
            'exp': datetime.datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, app.jwt_secret_key, 'HS256')
        return {"access_token": token, "token_type": "bearer"}

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
