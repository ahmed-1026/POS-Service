from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import hashlib
from typing import Dict
from api.transactions import router as transactions_router
from api.branches import router as branches_router
from api.sync import router as sync_router
from api.expenses import router as expenses_router

from db import actions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change to specific domains in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(transactions_router)
app.include_router(branches_router)
app.include_router(sync_router)
app.include_router(expenses_router)

class Category(BaseModel):
    id: int
    name: str
    date: str  
categories = []

# In-memory "database" of users for demonstration
FAKE_DB = {
    "test@example.com": {
        "password": hashlib.sha256("password123".encode()).hexdigest(),  # Hashed password
        "name": "Test User",
    }
}

# Pydantic models for request and response validation
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: Dict[str, str]

# Mock function to generate a "token" (replace with real JWT logic)
def generate_token(email: str) -> str:
    return hashlib.sha256(email.encode()).hexdigest()

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Validate user
    user = FAKE_DB.get(request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Check password (hashed comparison)
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
    if user["password"] != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate a token and return user info
    token = generate_token(request.email)
    return {
        "token": token,
        "user": {
            "name": user["name"],
            "email": request.email,
        },
    }


# @app.post("/categories/")
# def create_category(categories: List[Category]):
#     print("Received categories:")
#     for category in categories:
#         print(category)

@app.post("/categories")
async def receive_any_data(request: Request):
    try:
        # Read the raw data from the request
        data = await request.json()  # Parse incoming JSON data
        print("Received data:", data)
        
        # Return a success response
        return {"message": "Data received successfully", "data": data}
    except Exception as e:
        print(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Failed to process data")
    
@app.get("/categories/")
def get_categories():
    return categories

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)