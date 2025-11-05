from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class MealPlanCreate(BaseModel):
    meal_name: str
    timeslot: str

class MealPlanResponse(MealPlanCreate):
    id: int
    user_id: int
    class Config:
        orm_mode = True
