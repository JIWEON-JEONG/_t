from fastapi import Cookie, FastAPI, HTTPException, Security
from fastapi.openapi.models import APIKeyIn, SecurityScheme
from fastapi.security import APIKeyCookie
from controller import controller

app = FastAPI()

app.include_router(controller.router)

# APIKey 쿠키 보안 설정
cookie_scheme = APIKeyCookie(name="session_id")

# 세션 검증 함수 정의
def get_session_id(session_id: str = Security(cookie_scheme)):
    if not session_id:
        raise HTTPException(status_code=401, detail="인증되지 않았습니다")
    # 여기서 세션 유효성 검사 로직 추가 가능
    return session_id

# OpenAPI 스키마에 보안 설정 추가
app.openapi_components = {
    "securitySchemes": {
        "sessionAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "session_id"
        }
    }
}
app.openapi_security = [{"sessionAuth": []}]

# 보호된 경로 예시
@app.get("/protected")
def protected(session_id: str = Security(get_session_id)):
    return {"message": "Protected route", "session_id": session_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)