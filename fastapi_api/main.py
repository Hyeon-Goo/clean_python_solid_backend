from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def pong():
    return "pong"

# execute command in windows
# uvicorn main:app --reload
