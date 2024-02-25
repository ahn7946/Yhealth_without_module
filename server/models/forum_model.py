# from sqlalchemy import TEXT, Column, Integer, func
from sqlmodel import SQLModel, Field, Relationship, TEXT, func, Column, Integer
from typing import Optional, List
from datetime import datetime


class ForumModel(SQLModel, table=True):
    __tablename__ = "forum"
    id: int = Field(default=None, primary_key=True)
    user_id: str
    user_pwd: str
    title: str
    description: str = Field(sa_column=TEXT)
    hit: int = Field(default=0)
    like: int = Field(default=0)
    created_at: datetime = Field(default=func.now())
    modified_at: datetime = Field(default=func.now())
    comments: List['CommentModel'] = Relationship(back_populates="forum")

    def update_modified_at(self):
        self.modified_at = func.now()

    def increase_like(self):
        self.like += 1

    def increase_hit(self):
        self.hit += 1
