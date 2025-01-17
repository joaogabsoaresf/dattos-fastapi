from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    contact_name: str
    user_name: str
    client_phone: str
    owner_phone: str
    is_group: bool
    from_client: bool
    message: str
    message_time: datetime
    message_id: str
    client_id: str
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    
    class Config:
        from_attributes = True
        
class SessionsBase(BaseModel):
    status: str
    owner_phone: str
    intance_id: str
    momment: datetime
    
class SessionsCreate(SessionsBase):
    pass

class Sessions(SessionsBase):
    id: int
    
    class Config:
        from_attributes = True