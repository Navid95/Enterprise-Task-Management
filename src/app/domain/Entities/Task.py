from pydantic import Field, model_validator
from datetime import datetime, timedelta
from uuid import UUID
from src.app.domain.Entities.base import Base
from src.app.domain.Entities.task_exceptions import InvalidStartEndDateRange

_DEFAULT_TASK_DURATION_MINUTES_ = 1 * 24 * 60


def end_date_time_generator():
    return datetime.now() + timedelta(minutes=_DEFAULT_TASK_DURATION_MINUTES_)


class Task(Base):
    title: str = Field(max_length=50)
    description: str = Field(max_length=250, default="")
    owner_id: UUID
    assignee_id: UUID = Field(default=None)
    start: datetime = Field(default_factory=datetime.now)
    end: datetime = Field(default_factory=end_date_time_generator)

    @model_validator(mode="after")
    def validate_start_end(self):
        if self.start >= self.end:
            raise InvalidStartEndDateRange.as_pydantic_error(start_date=self.start, end_date=self.end)
        return self

