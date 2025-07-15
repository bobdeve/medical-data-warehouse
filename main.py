from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
import database


app = FastAPI(title="📊 Medical Product Intelligence API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = Query(10), db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

@app.get("/api/channels/{channel_id}/activity", response_model=schemas.ChannelActivity)
def channel_activity(channel_id: int, db: Session = Depends(get_db)):
    result = crud.get_channel_activity(db, channel_id)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found.")
    return result


@app.get("/api/search/messages", response_model=List[schemas.MessageSearch])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Product Intelligence API. Use /docs to explore available endpoints."}

