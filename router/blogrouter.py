from fastapi import APIRouter,Depends
from db.dbConnection import get_db
from controller.blogContrroller import BlogController
from model.basemodel import BlogSchema
from sqlalchemy.orm import Session
from fastapi import status
class BlogRoutes:

    def __init__(self):
        self.app = APIRouter()
        self.blog_controller = BlogController()
        self.__add_routes()

    def __add_routes(self):
        self.app.add_api_route(
            path="/add-blog",
            endpoint=self.add_blog,
            methods=["POST"]
        )
        self.app.add_api_route(
            path="/get-blog-list",
            endpoint=self.get_blog_list,
            methods=["GET"]
        )
        self.app.add_api_route(
            path="/delete-blog/{blog_id}",
            endpoint=self.delete_blog,
            methods=["DELETE"]
        )

    async def add_blog(self, post: BlogSchema,db: Session = Depends(get_db)):
        try:
            res=self.blog_controller.add_blog(
                title=post.title,
                content=post.content,
                db=db
            )
            return {"message":res, "status":status.HTTP_201_CREATED}
        except Exception as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
    async def get_blog_list(self,db: Session = Depends(get_db)):
        try:
            res=self.blog_controller.get_blog_list(
                db=db
            )
            return {"data":res, "status":status.HTTP_200_OK}
        except Exception as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR 
    async def delete_blog(self, blog_id: int, db: Session = Depends(get_db)):
        try:
            res = self.blog_controller.delete_blog(
                blog_id=blog_id,
                db=db
            )
            return {"message": res, "status": status.HTTP_200_OK}
        except Exception as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR 