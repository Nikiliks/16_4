from fastapi import FastAPI, status, Body, Path, HTTPException
from typing import Annotated
from typing import List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def return_dict() -> List[User]:
    return users

@app.post("/user/{username}/{age}")
async def append_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='Example')],
                    age: Annotated[int, Path(le=120, ge=18, description='Enter age', examples='18')])-> User:
    user_id = (users[-1].id + 1) if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}")
async def update_users(user_id: Annotated[int, Path(gt=0, lt=100, description='Enter User ID', examples='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', examples='Example')],
                    age: Annotated[int, Path(le=120, ge=18, description='Enter age', examples='18')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete( '/user/{user_id}')
async def delete_users(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter user id', examples='1')]) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")



#Запуск: uvicorn module_16_4:app --reload


