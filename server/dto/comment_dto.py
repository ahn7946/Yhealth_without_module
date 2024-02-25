from pydantic import BaseModel


class CommentCreateDTO(BaseModel):
    forum_id: int
    user_id: str
    user_pwd: str
    description: str


class CommentUpdateDTO(BaseModel):
    content: str
