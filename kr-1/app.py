from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models import User, UserAge, Feedback

my_app = FastAPI()

current_user = User(name="Питер Стил", id=1)

feedbacks = []

@my_app.get("/")
def read_root():
    return FileResponse("index.html")

class CalculateRequest(BaseModel):
    num1: int
    num2: int

@my_app.post("/calculate")
def calculate(data: CalculateRequest):
    return {"result": data.num1 + data.num2}

@my_app.get("/users")
def get_users():
    return current_user

@my_app.post("/user")
def create_user(user: UserAge):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18
    }

@my_app.post("/feedback")
def submit_feedback(feedback: Feedback):
    feedbacks.append(feedback.model_dump())
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}