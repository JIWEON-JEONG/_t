from functools import wraps
from sqlalchemy.orm import Session
from configuration.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db  # db 세션을 반환
    finally:
        db.close()  # 요청이 끝나면 db 세션을 닫음

def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # db가 kwargs에 이미 있으면 그 값을 사용
        db: Session = kwargs.get('db')

        try:
            # db를 함수에 전달하여 실행
            result = await func(*args, **kwargs)  
            db.commit()  # 트랜잭션 커밋
            return result
        except Exception as e:
            db.rollback()  # 예외가 발생하면 롤백
            raise e
        finally:
            # db 세션이 새로 생성된 세션이라면 닫아야 합니다.
            if db is not kwargs.get('db'):
                db.close()

    return wrapper

