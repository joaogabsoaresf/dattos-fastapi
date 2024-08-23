from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Messages(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer,primary_key=True,nullable=False)
    contact_name = Column(String,nullable=False)
    user_name = Column(String,nullable=False)
    client_phone = Column(String,nullable=False)
    owner_phone = Column(String,nullable=False)
    is_group = Column(Boolean,nullable=False,default=False)
    from_client = Column(Boolean,nullable=False,default=False)
    message_time = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
