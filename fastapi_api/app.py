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


class FollowModel(BaseModel):
    id: int
    follow: int


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
    json_response = {
        "message": "",
        "status_code": 200
    }
    if user_id not in app.users:
        json_response["message"] = '사용자가 존재하지 않습니다'
        json_response["status_code"] = 400
        return json_response
    if len(tweet_str) > 300:
        json_response["message"] = '300자를 초과했습니다.'
        json_response["status_code"] = 400
        return json_response
    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet_str
    })
    return json_response


@app.post("/follow")
async def follow(follow_body: FollowModel):
    user_id = follow_body.id
    user_id_to_follow = follow_body.follow
    json_response = {
        "message": "",
        "status_code": 200
    }
    if user_id not in app.users or user_id_to_follow not in app.users:
        json_response["message"] = '시용자가 존재하지 않습니다.'
        json_response["status_code"] = 400
    user: dict = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)
    return JSONResponse(user)


@app.post("/unfollow")
async def unfollow(follow_body: FollowModel):
    user_id = follow_body.id
    user_id_to_follow = follow_body.follow
    json_response = {
        "message": "",
        "status_code": 200
    }
    if user_id not in app.users or user_id_to_follow not in app.users:
        json_response["message"] = '시용자가 존재하지 않습니다.'
        json_response["status_code"] = 400
    user: dict = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)
    return JSONResponse(user)


@app.get('/timeline/{user_id}')
async def timeline(user_id: int):
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다', 400
    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet_str for tweet_str in app.tweets if tweet_str['user_id'] in follow_list]
    return JSONResponse({
        'user_id': user_id,
        'timeline': timeline
    })










# execute command in windows
# uvicorn main:app --reload
