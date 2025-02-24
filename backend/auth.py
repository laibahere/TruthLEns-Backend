from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from database import users_collection

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI Router
router = APIRouter()

# User model
class UserSignup(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Signup route
@router.post("/signup")
def signup(user: UserSignup):
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Hash the password before storing it
    hashed_password = hash_password(user.password)

    # Insert user into the database
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    users_collection.insert_one(new_user)

    return {"message": "User registered successfully!"}

# Login route
@router.post("/login")
def login(user: UserLogin):
    # Check if user exists
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    # Verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    return {"message": "Login successful!", "user": {"username": db_user["username"], "email": db_user["email"]}}
