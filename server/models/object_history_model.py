from sqlmodel import SQLModel, Field
from datetime import datetime


class ObjectHistoryModel1(SQLModel, table=True):
    __tablename__ = "object_history_1"
    id: int = Field(default=None, primary_key=True)
    current_person: int
    updated_at: datetime


class ObjectHistoryModel2(SQLModel, table=True):
    __tablename__ = "object_history_2"
    id: int = Field(default=None, primary_key=True)
    current_person: int
    updated_at: datetime
