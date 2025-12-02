from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.dbConnection import get_db
from model.basemodel import UserCreate,UserLogin, Token
from model.modles import User
from auth.hash import hash_password, verify_password
from auth.jwt import create_access_token
from controller.userController import UserController


class UserRoutes:

    def __init__(self):
        self.app = APIRouter()
        self.blog_controller = UserController()
        self.__add_routes()

    def __add_routes(self):
        self.app.add_api_route(
            path="/add-user",
            endpoint=self.add_user,
            methods=["POST"]
        )
        self.app.add_api_route(
            path="/login",
            endpoint=self.login,
            methods=["POST"]
        )
    
    

    async def add_user(self, user: UserCreate, db: Session = Depends(get_db)):
        try:
            db_user = db.query(User).filter(User.email == user.email).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            hashed_pwd = hash_password(user.password)      
            res = self.blog_controller.add_user(
                username=user.username,
                email=user.email,
                password=hashed_pwd,
                db=db
            )
            return {"message": res, "status": status.HTTP_201_CREATED}
        except Exception as e:
            return {"error": str(e),"status": status.HTTP_500_INTERNAL_SERVER_ERROR }

    async def login(self, user: UserLogin, db: Session = Depends(get_db)):
        try:
            res=self.blog_controller.login(
                email=user.email,
                password=user.password,
                db=db
            )
            return {"access_token": res, "token_type": "bearer","status": status.HTTP_201_CREATED}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e),"status" :status.HTTP_500_INTERNAL_SERVER_ERROR}


