from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.modles import User
from auth.hash import hash_password
from auth.hash import verify_password



class UserController:
    def add_user(self, username: str, email: str, password: str, db: Session):
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(username=username, email=email, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return "User created successfully"
    def login(self, email: str, password: str, db: Session):
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user or not verify_password(password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        from auth.jwt import create_access_token
        token = create_access_token({"user_id": db_user.id})
        return token    
