from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    message_type: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    response: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
