from datetime import datetime
import enum

from pydantic import BaseModel, PrivateAttr, computed_field

class Priority(enum.Enum): 
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TodoRequest(BaseModel): 
    name: str
    description: str
    deadline: datetime
    priority: Priority

class TodoResponse(BaseModel): 
    _id: int = PrivateAttr() # -> private field
    _user_id: int = PrivateAttr() # -> private field
    name: str
    description: str
    dead_line: datetime
    priority: Priority = Priority.LOW
    created_at: datetime = datetime.now()

    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self._user_id = data.get('_user_id')

    @computed_field
    @property
    def remaining_time(self) -> datetime:
        return self.dead_line - self.created_at
