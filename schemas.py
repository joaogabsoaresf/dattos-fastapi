from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    contact_name: str
    user_name: str
    client_phone: str
    owner_phone: str
    is_group: bool
    message_time: datetime
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    
    class Config:
        from_attributes = True