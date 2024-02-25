from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ForumCreateDTO(BaseModel):
    user_id: str
    user_pwd: str
    title: str
    description: str


class ForumUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    modified_at: Optional[datetime] = None
