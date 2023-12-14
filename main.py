from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.user import user_router
from domain.attendance import attendance_router

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.include_router(user_router.router)
app.include_router(attendance_router.router)
