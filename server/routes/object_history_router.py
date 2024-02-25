from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import Session

from server.connect.connection import get_session
from server.models.object_history_model import ObjectHistoryModel1, ObjectHistoryModel2

object_history_router = APIRouter()


@object_history_router.get("")
@object_history_router.get("/")
async def retrieve_object_histories(session: Session = Depends(get_session)):
    latest_history_1 = session.query(ObjectHistoryModel1).order_by(desc(ObjectHistoryModel1.id)).first()
    latest_history_2 = session.query(ObjectHistoryModel2).order_by(desc(ObjectHistoryModel2.id)).first()

    return {
        "gym1_count": latest_history_1.current_person,
        "gym2_count": latest_history_2.current_person,
    }