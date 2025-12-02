from fastapi import FastAPI
import uvicorn
from model.modles import Blog
from db.dbConnection import Base, engine
from router.blogrouter import BlogRoutes
from router.userrouter import UserRoutes
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()
Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(UserRoutes().app, tags=["User"])
app.include_router(BlogRoutes().app, tags=["Blog"])



if '__main__' == __name__:
  

    uvicorn.run(app, host='0.0.0.0', port=8000)
