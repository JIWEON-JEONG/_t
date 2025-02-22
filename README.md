## 실행방법

1. git clone https://github.com/JIWEON-JEONG/_t.git
2. cd ./_t
3. docker-compose up -d
4. python3 -m venv .venv
5. source .venv/bin/activate
7. pip install -r requirements.txt
8. uvicorn main:app --reload --proxy-headers

## API 스펙 (Swagger)
실행 시킨 후 http://localhost:8000/docs 접속.

## 구조

### controller 
- presentation layer
- 클라이언트 요청, 응답에 대한 스펙 구현

### application 
- usecase 스펙 구현 
- domain or domain_service 들을 facade 하여 요구사항 구현.

### domain
 - 비즈니스, 정책들을 정의 및 구현
 - 도메인 독립적인 의존성만을 가지며 (orm 의존성 제외), 외부 의존성을 최대한 차단.

### repository
 - persistence layer
 - 데이터베이스 등과 같은 3rd 파티 상호작용 구현체.

### common 
- 프로젝트 전반에서 공통으로 사용되는 기능 구현.
- 공통 기능.

### dto 
- data-transform-object
- 의존성 관리를 위해 디렉토리 분리

  

