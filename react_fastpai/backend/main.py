from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정 (React와 연동 시 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JournalEntry(BaseModel):
    content: str
    is_public: bool

@app.post("/save")
async def save_journal(entry: JournalEntry):
    print("저장 요청됨:", entry)
    # 실제 DB 저장 로직을 여기에 추가
    return {"message": "저장 완료! fastapi"}
