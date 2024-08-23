import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Any, Dict
import crud, models, schemas
from database import SessionLocal, engine
from format_request import FormatMessage, FormatSessions

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def validate_api_token(z_api_token: str = Header(...)):
    if z_api_token != os.getenv('Z_API_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
            headers={"WWW-Authenticate": "Bearer"},
        )



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/message/", response_model=schemas.Message)
def create_message(data: Dict[str, Any], db: Session = Depends(get_db), token: str = Depends(validate_api_token)):
    message_data = FormatMessage(data).message_fields()
    message = schemas.MessageCreate(**message_data)
    return crud.create_message(db=db, message=message)

@app.get("/message/", response_model=list[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(validate_api_token)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages

@app.get("/message/{message_id}", response_model=schemas.Message)
def read_user(message_id: int, db: Session = Depends(get_db), token: str = Depends(validate_api_token)):
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.post("/sessions/", response_model=schemas.Sessions)
def create_message(data: Dict[str, Any], db: Session = Depends(get_db), token: str = Depends(validate_api_token)):
    session_data = FormatSessions(data).session_fields()
    session = schemas.SessionsCreate(**session_data)
    return crud.create_session_register(db=db, session=session)