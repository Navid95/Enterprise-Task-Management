from pydantic import Field
from datetime import datetime, timedelta
from src.app.domain.Entities.base import Base
from src.app.domain.auth.users import User

_DEFAULT_TASK_DURATION_MINUTES_ = 1 * 24 * 60


def end_date_time_generator():
    return datetime.now() + timedelta(minutes=_DEFAULT_TASK_DURATION_MINUTES_)


class Task(Base):
    title: str = Field(max_length=50)
    description: str | None = Field(max_length=250)
    owner: User
    assignee: User | None
    start: datetime = Field(default_factory=datetime.now)
    end: datetime = Field(default_factory=end_date_time_generator)
