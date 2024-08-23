from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict
import crud, models, schemas
from database import SessionLocal, engine
from format_request import FormatMessage

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/message/", response_model=schemas.Message)
def create_message(data: Dict[str, Any], db: Session = Depends(get_db)):
    message_data = FormatMessage(data).message_fields()
    message = schemas.MessageCreate(**message_data)
    return crud.create_message(db=db, message=message)

@app.get("/message/", response_model=list[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages

@app.get("/message/{message_id}", response_model=schemas.Message)
def read_user(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message