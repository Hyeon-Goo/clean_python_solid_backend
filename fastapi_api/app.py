from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class SignUpModel(BaseModel):
    name: str
    email: str
    password: str
    profile: str


class TweetModel(BaseModel):
    id: int
    tweet_str: str


app = FastAPI()
app.users = {}
app.id_count = 1
app.tweets = []


@app.get("/ping")
async def pong():
    return "pong"


@app.post("/sign-up")
async def sign_up(sign_up_body: SignUpModel):
    sign_up_dict = sign_up_body.dict()
    sign_up_dict['id'] = app.id_count
    app.users[app.id_count] = sign_up_dict
    app.id_count = app.id_count + 1
    return JSONResponse(sign_up_dict)


@app.post("/tweet")
async def tweet(tweet_body: TweetModel):
    user_id = tweet_body.id
    tweet_str = tweet_body.tweet_str
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400
    if len(tweet_str) > 300:
        return '300자를 초과했습니다.', 400
    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet_str
    })
    return '', 200






# execute command in windows
# uvicorn main:app --reload
