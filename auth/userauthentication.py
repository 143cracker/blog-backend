from functools import wraps
from fastapi import Request, HTTPException,FastAPI,status,Depends
import time
import base64, json
from db.dbConnection import get_db
from  auth.hash import verify_password
from model.modles import User
from auth.jwt import decode_access_token
from sqlalchemy.orm import Session

def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    return user
application = app = FastAPI()
def jwt_auth_required(f):
    @wraps(f)
    def authenticate( *args, **kwargs):
        authtoken=''
        start_time = time.time()
        request = kwargs.get('request')
        req_path = request.scope.get('path')[1:]
        if 'Authorization' not in request.headers or 'authorization' not in request.headers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credentials not sent")

        if 'Authorization' in request.headers or 'authorization' in request.headers:
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                authtoken = token
            else:
                token = request.headers['authorization']
                authtoken = token
            if authtoken:
                try:
                    token = authtoken.split(" ")[1]
                    payload = decode_access_token(token)
                    if not payload:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
                      
                    username = payload.get("username")
                    userpassword = payload.get("password")
                    get_user_by_username_func = Depends(get_user_by_username)
                    user = get_user_by_username_func(username=username)
                    if not user or not verify_password(userpassword , user.password):
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")         
                   
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credentials not sent")

       
        return f(*args, **kwargs)

    return authenticate










  