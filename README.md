## 실행방법

1. git clone https://github.com/JIWEON-JEONG/_t.git
2. cd ./_t
3. docker-compose up -d
4. python3 -m venv .venv
5. source .venv/bin/activate
7. pip install -r requirements.txt
8. uvicorn main:app --reload --proxy-headers

## API 스펙 및 E2E 테스트 가능 링크 
http://localhost:8000/docs
