from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from server.connect.connection import get_session
from server.models.forum_model import ForumModel
from server.models.comment_model import CommentModel
from server.dto.forum_dto import ForumCreateDTO, ForumUpdateDTO

# from ..connect.connection import get_session
# from ..models.forum_model import ForumModel
# from ..models.comment_model import CommentModel
# from ..dto.forum_dto import ForumCreateDTO, ForumUpdateDTO

forum_router = APIRouter(tags=["Forums"])


@forum_router.get("", response_model=List[ForumModel])
@forum_router.get("/", response_model=List[ForumModel])
async def retrieve_all_forums(session: Session = Depends(get_session)) -> List[ForumModel]:
    return session.query(ForumModel).all()


@forum_router.post("", status_code=status.HTTP_201_CREATED)
@forum_router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_forum(new_forum: ForumCreateDTO, session: Session = Depends(get_session)) -> dict:
async def create_forum(new_forum: ForumCreateDTO,
                       session: Session = Depends(get_session)) -> dict:
    forum = ForumModel(**new_forum.dict())
    session.add(forum)
    session.commit()
    session.refresh(forum)
    return {"message": "Forum created successfully"}


@forum_router.get("/{id}", response_model=ForumModel)
@forum_router.get("/{id}/", response_model=ForumModel)
async def read_forum(id: int,
                     session: Session = Depends(get_session)) -> ForumModel:
    forum = session.query(ForumModel).filter(ForumModel.id == id).first()
    if not forum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Forum with supplied ID does not exist")
    forum.increase_hit()
    session.commit()
    session.refresh(forum)
    return forum


@forum_router.put("/{id}")
@forum_router.put("/{id}/")
async def update_forum(id: int,
                       update_data: ForumUpdateDTO,
                       session: Session = Depends(get_session)) -> dict:
    forum = session.query(ForumModel).filter(ForumModel.id == id).first()
    if not forum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Forum with supplied ID does not exist")
    for field, value in update_data.dict().items():
        if value is not None:
            setattr(forum, field, value)
    forum.update_modified_at()
    session.commit()
    session.refresh(forum)
    return {"message": "Forum updated successfully"}


@forum_router.delete("/{id}")
@forum_router.delete("/{id}/")
async def delete_forum(id: int,
                       session: Session = Depends(get_session)) -> dict:
    forum = session.query(ForumModel).filter(ForumModel.id == id).first()
    if not forum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Forum with supplied ID does not exist")
    comments = session.query(CommentModel).filter(CommentModel.forum_id == id).all()
    if comments:
        for comment in comments:
            session.delete(comment)

    session.delete(forum)
    session.commit()

    return {"message": "Forum deleted successfully"}


@forum_router.put("/{id}/like")
@forum_router.put("/{id}/like/")
async def like_forum(id: int,
                     session: Session = Depends(get_session)) -> dict:
    forum = session.query(ForumModel).filter(ForumModel.id == id).first()
    if not forum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Forum with supplied ID does not exist")
    forum.increase_like()
    session.commit()
    session.refresh(forum)
    return {"message": "Forum liked successfully"}
