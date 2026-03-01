from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import secrets

app = FastAPI(title="FocusFlow API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Data Models =====
class User(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    token: str

# ===== In-Memory Storage =====
users_db: Dict[str, dict] = {}
tokens_db: Dict[str, str] = {}  # token -> username mapping

# ===== Helper Functions =====
def generate_token():
    """Generate a simple token"""
    return secrets.token_urlsafe(32)

def verify_token(token: str) -> str:
    """Verify token and return username"""
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens_db[token]

# ===== Authentication Endpoints =====

@app.post("/auth/signup", response_model=UserResponse)
def signup(user: User):
    """Register a new user"""
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if any(u["email"] == user.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user (in production, hash password!)
    users_db[user.username] = {
        "email": user.email,
        "password": user.password  # NOT SECURE - for demo only
    }
    
    # Generate token
    token = generate_token()
    tokens_db[token] = user.username
    
    return UserResponse(
        username=user.username,
        email=user.email,
        token=token
    )

@app.post("/auth/login", response_model=UserResponse)
def login(credentials: LoginRequest):
    """Login user"""
    if credentials.username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[credentials.username]
    if user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token
    token = generate_token()
    tokens_db[token] = credentials.username
    
    return UserResponse(
        username=credentials.username,
        email=user["email"],
        token=token
    )

@app.post("/auth/logout")
def logout(token: str):
    """Logout user"""
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    del tokens_db[token]
    return {"message": "Logged out successfully"}

# ===== User Endpoints =====

@app.get("/user/profile")
def get_profile(token: str):
    """Get current user profile"""
    username = verify_token(token)
    user = users_db[username]
    
    return {
        "username": username,
        "email": user["email"]
    }

@app.put("/user/profile")
def update_profile(token: str, email: Optional[str] = None):
    """Update user profile"""
    username = verify_token(token)
    
    if email:
        # Check if email is already in use
        if any(u["email"] == email for u in users_db.values()):
            raise HTTPException(status_code=400, detail="Email already in use")
        users_db[username]["email"] = email
    
    return {
        "username": username,
        "email": users_db[username]["email"]
    }

# ===== Health Check =====

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api": "FocusFlow API"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FocusFlow API",
        "version": "1.0.0",
        "docs": "/docs"
    }
