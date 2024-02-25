from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from server.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO
from server.models.comment_model import CommentModel
from server.connect.connection import get_session

# from ..dto.comment_dto import CommentCreateDTO, CommentUpdateDTO
# from ..models.comment_model import CommentModel
# from ..connect.connection import get_session

comment_router = APIRouter(tags=["Comments"])


@comment_router.get("", response_model=List[CommentModel])
@comment_router.get("/", response_model=List[CommentModel])
async def retrieve_all_comments(session: Session = Depends(get_session)) -> List[CommentModel]:
    return session.query(CommentModel).all()


@comment_router.post("", status_code=status.HTTP_201_CREATED)
@comment_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(new_comment: CommentCreateDTO, session: Session = Depends(get_session)) -> dict:
    comment = CommentModel(**new_comment.dict())
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return {"message": "Comment created successfully"}


@comment_router.get("/{forum_id}", response_model=List[CommentModel])
@comment_router.get("/{forum_id}/", response_model=List[CommentModel])
async def read_comment(forum_id: int,
                       session: Session = Depends(get_session)) -> List[CommentModel]:
    comments = session.query(CommentModel).filter(CommentModel.forum_id == forum_id).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment with supplied ID does not exist"
                            )
    return comments


@comment_router.put("/{id}")
@comment_router.put("/{id}/")
async def update_comment(id: int,
                         update_data: CommentUpdateDTO,
                         session: Session = Depends(get_session)) -> dict:
    comment = session.query(CommentModel).filter(CommentModel.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment with supplied ID does not exist"
                            )

    for field, value in update_data.dict().items():
        if value is not None:
            setattr(comment, field, value)

    session.commit()
    session.refresh(comment)  # 변경 사항을 확인하기 위해 새로고침
    return {"message": "Comment updated successfully"}


@comment_router.delete("/{id}")
@comment_router.delete("/{id}/")
async def delete_comment(id: int,
                         session: Session = Depends(get_session)) -> dict:
    comment = session.query(CommentModel).filter(CommentModel.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment with supplied ID does not exist"
                            )

    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted successfully"}
