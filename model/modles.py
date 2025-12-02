from sqlalchemy import Column, Integer, String, Text,DateTime,ForeignKey
from db.dbConnection import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
   
    blogs = relationship("Blog", back_populates="author", cascade="all, delete")
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    date = Column(String(50))
    author = relationship("User", back_populates="blogs")
    