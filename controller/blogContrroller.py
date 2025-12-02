from datetime import datetime
from model.modles import Blog

class BlogController:
    def add_blog(self, title: str, content: str, db):
        # Logic to add a blog post
        new_post = Blog(
        title=title,
        content=content,
        date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return "Blog added"
    def get_blog_list(self, db):
        # Logic to get list of blog posts
        blogs = db.query(Blog).all()
        return blogs    
    def delete_blog(self, blog_id: int, db):
        # Logic to delete a blog post
        blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if blog:
            db.delete(blog)
            db.commit()
            return "Blog deleted"
        else:
            return "Blog not found" 