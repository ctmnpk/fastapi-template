from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

class Priority(Enum): 
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Todo(BaseModel): 
    _id: UUID # -> private field
    _user_id: UUID # -> private field
    description: str
    dead_line: datetime
    priority: Priority = Priority.LOW
    created_at: datetime = datetime.now()
