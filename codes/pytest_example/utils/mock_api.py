import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post("/login")
def login(data: Login):
    if data.username == "admin" and data.password == "password":
        resp = JSONResponse(
            content={"message": "Login successful", "status_code": 200, "token": "hello"},
            status_code=200
        )
    else:
        resp = JSONResponse(
            content={"message": "Invalid credentials", "status_code": 400,  "token": None}, 
            status_code=400
        )
    return resp

uvicorn.run(app, host="127.0.0.1", port=8000)
    