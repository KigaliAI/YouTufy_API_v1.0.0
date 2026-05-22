#api/routes/reset.py
from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from utils.emailer import send_email
from utils.tokens import generate_token
from backend.database import SessionLocal
from backend.models import User
import os

router = APIRouter()
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reset-password")
def request_password_reset(email: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        print(f"🔍 Reset requested for unknown email: {email}")
        return {"message": "If this email is registered, a reset link has been sent."}

    token = generate_token(email)
    reset_link = f"{FRONTEND_URL}/auth/verify-token.html?token={token}"

    send_email(
        to_email=email,
        subject="Reset Your YouTufy Password",
        content=f"Click here to reset your password: <a href='{reset_link}'>Reset Password</a>"
    )

    return {"message": "If this email is registered, a reset link has been sent."}

@router.post("/verify-token.html")
def reset_password_from_token(
    token: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        email = verify_token(token)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user")
        user.hashed_password = hash_password(new_password)
        db.commit()
        return RedirectResponse(url="/auth/login-form.html", status_code=302)
    except Exception as e:
        print(f"⚠️ Token verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid or expired token")
