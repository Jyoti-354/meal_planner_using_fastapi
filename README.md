# Meal Planner API

This FastAPI project lets users plan and track daily meals with reminders.

## 🛠 Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic bcrypt python-jose passlib
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```

### 4. Open in Browser
Visit: http://127.0.0.1:8000/docs

You can register users, create meal plans, and fetch them.

### 5. Example Endpoints

- **POST** `/register` – Register a new user
- **POST** `/login` – Login an existing user (verify username and password)
- **POST** `/mealplan` – Add a meal plan (requires user_id)
- **GET** `/mealplan/{user_id}` – Fetch all meals for a user
- **PUT** `/meal-plans/{meal_id}` – Update an existing meal plan (edit meal name or timeslot)
- **DELETE** `/meal-plans/{meal_id}` – Delete a meal plan permanently



---
Database: SQLite (auto-created file `mealplanner.db`)
