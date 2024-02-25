from sqlmodel import SQLModel, Field, Relationship, TEXT, func, Column, Integer
from datetime import datetime

class CommentModel(SQLModel, table=True):
    __tablename__ = "comment"
    id: int = Field(default=None, primary_key=True)
    forum_id: int = Field(foreign_key="forum.id")
    user_id: str
    user_pwd: str
    description: str
    created_at: datetime = Field(default=func.now())
    modified_at: datetime = Field(default=func.now())
    forum: 'ForumModel' = Relationship(back_populates="comments")

    def update_modified_at(self):
        self.modified_at = func.now()