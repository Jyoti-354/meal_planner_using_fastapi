from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models, schemas, crud
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Planner API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Register a new user
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Ensure password length < 72
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long, please use less than 72 characters.")
    return crud.create_user(db, user)

@app.post("/login")
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not crud.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"message": f"Welcome back, {db_user.username}!"}



# ✅ Create meal plan
@app.post("/mealplan", response_model=schemas.MealPlanResponse)
def create_meal(meal: schemas.MealPlanCreate, user_id: int, db: Session = Depends(get_db)):
    reminder_time = datetime.now().strftime("%H:%M:%S")
    print(f"[Reminder] Hey user {user_id}, please update your {meal.timeslot} meal status!")
    return crud.create_meal_plan(db, meal, user_id)

# ✅ Get all meals for a user
@app.get("/mealplan/{user_id}", response_model=list[schemas.MealPlanResponse])
def get_meals(user_id: int, db: Session = Depends(get_db)):
    return crud.get_meal_plans(db, user_id)


# ✅ Update an existing meal plan
@app.put("/meal-plans/{meal_id}")
def update_meal_plan(meal_id: int, meal: schemas.MealPlanCreate, db: Session = Depends(get_db)):
    db_meal = db.query(models.MealPlan).filter(models.MealPlan.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    # Update fields
    db_meal.meal_name = meal.meal_name
    db_meal.timeslot = meal.timeslot

    db.commit()
    db.refresh(db_meal)
    return {"message": "Meal plan updated successfully", "meal": db_meal}


# ✅ Delete a meal plan
@app.delete("/meal-plans/{meal_id}")
def delete_meal_plan(meal_id: int, db: Session = Depends(get_db)):
    db_meal = db.query(models.MealPlan).filter(models.MealPlan.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    db.delete(db_meal)
    db.commit()
    return {"message": "Meal plan deleted successfully"}
