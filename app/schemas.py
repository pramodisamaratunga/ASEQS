from pydantic import BaseModel

class MessageBase(BaseModel):
    message_type: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    response: str | None = None

    class Config:
        orm_mode = True
