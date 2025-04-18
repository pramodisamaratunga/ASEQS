from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.database import SessionLocal, engine
from app import models, schemas

# Tạo bảng trong database nếu chưa có
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency lấy session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Gọi LLM từ LM Studio
async def send_to_llm(message_type: str, content: str):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [{"role": message_type, "content": content}],
        "max_tokens": 200
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']

# Tạo message mới
@app.post("/messages/", response_model=schemas.MessageResponse)
async def create_message(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    response_llm = await send_to_llm(msg.message_type, msg.content)
    db_msg = models.Message(
        message_type=msg.message_type,
        content=msg.content,
        response=response_llm
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

# Lấy message theo id
@app.get("/messages/{msg_id}", response_model=schemas.MessageResponse)
def read_message(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(models.Message).filter(models.Message.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg

# Lấy toàn bộ message (phân trang)
@app.get("/messages/", response_model=list[schemas.MessageResponse])
def read_all_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Message).offset(skip).limit(limit).all()
