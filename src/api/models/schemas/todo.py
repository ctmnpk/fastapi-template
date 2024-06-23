from pydantic import BaseModel, computed_field
from pytz import timezone

from datetime import datetime, timedelta
from typing import Annotated, Optional

from models.enums import Priority

local_timezone = timezone("America/Sao_Paulo")


class TodoBase(BaseModel):
    title: Annotated[str, "Title"]
    description: Annotated[str, "Description"]
    dead_line: Annotated[datetime, "Deadline"]
    priority: Optional[Annotated[Priority, "Priority"]] = Priority.LOW


class TodoCreateRequest(TodoBase):
    pass


class TodoUpdateRequest(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: Annotated[int, "Todo ID"]

    @computed_field
    @property
    def remaining_time(self) -> dict:
        remaining = self.dead_line - datetime.now()

        if remaining.total_seconds() < 0:
            remaining = timedelta(0)

        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        remaining_time_dict = {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

        return remaining_time_dict
