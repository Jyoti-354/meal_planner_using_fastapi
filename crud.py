from sqlalchemy.orm import Session
import models, schemas
import bcrypt


# ✅ Safe helper functions
def hash_password(password: str) -> str:
    # convert to bytes and truncate if necessary
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8")[:72], hashed_password.encode("utf-8"))
    except Exception:
        return False


# ✅ CRUD functions
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user


def create_meal_plan(db: Session, meal: schemas.MealPlanCreate, user_id: int):
    db_meal = models.MealPlan(**meal.dict(), user_id=user_id)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


def get_meal_plans(db: Session, user_id: int):
    return db.query(models.MealPlan).filter(models.MealPlan.user_id == user_id).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
