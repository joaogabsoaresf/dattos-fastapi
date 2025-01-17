import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Any, Dict
import crud, models, schemas
from database import SessionLocal, engine
from format_request import FormatMessage, FormatSessions
from bigquery import BigQueryClient
from utils import more_than_twenty_four_hours, more_than_seventy_two_hours, query_datetime_format
import bigquery

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
    pass
    # if z_api_token != os.getenv('Z_API_TOKEN'):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid API token",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
def get_bigquery():
    client = BigQueryClient()
    try:
        yield client
    finally:
        return



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/message/", response_model=schemas.Message)
def create_message(data: Dict[str, Any], db: Session = Depends(get_db), token: str = Depends(validate_api_token)):
    message_data = FormatMessage(data).message_fields()
    message = schemas.MessageCreate(**message_data)
    save = crud.create_message(db=db, message=message)
    client = BigQueryClient(table_id='adm-lake.CS_01_Raw.whastapp_registros', dataset_id='adm-lake.CS_01_Raw')
    client.insert_row(message_data)
    return save

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
def create_session(data: Dict[str, Any], db: Session = Depends(get_db), token: str = Depends(validate_api_token)):
    session_data = FormatSessions(data).session_fields()
    session = schemas.SessionsCreate(**session_data)
    return crud.create_session_register(db=db, session=session)

@app.post("/bigquery/")
def create_row(data: Dict[str, Any]):
    message_data = FormatMessage(data).message_fields()
    client = BigQueryClient(table_id='adm-lake.CS_01_Raw.whastapp_registros', dataset_id='adm-lake.CS_01_Raw')
    errors = client.insert_row(message_data)
    if errors:
        return {'status':'erro', 'errors':errors}
    return {'status':'success'}

@app.post("/alert/whatsapp/")
def list_pending():
    client = BigQueryClient(table_id='adm-lake.CS_01_Raw.whastapp_registros', dataset_id='adm-lake.CS_01_Raw')
    message_thread = client.list_rows()
    alert_client = BigQueryClient(table_id='adm-lake.CS_01_Raw.Alertas_Whatsapp', dataset_id='adm-lake.CS_01_Raw')
    for message in message_thread:
        message['message_time_str'] = format_message_time(message['message_time'])
        if is_over_sla(message.get('message_time_str')) and not client.message_in_contact_window(message.get('client_phone'), query_datetime_format(message.get('message_time'))): 
            row_data = client.get_alert_row(message)
            alert_client.insert_row_alert(row_data)
    return {'status':'success'}


def format_message_time(message_time):
    formatted_time = message_time.strftime("%d/%m/%y %H:%M:%S")
    return formatted_time


def is_over_sla(datetime):
    if more_than_seventy_two_hours(datetime):
        return True
    return more_than_twenty_four_hours(datetime)

