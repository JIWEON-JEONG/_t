from functools import wraps
from sqlalchemy.orm import Session
from configuration.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: Session = SessionLocal()
        try:
            kwargs['db'] = session
            result = await func(*args, **kwargs)
            session.commit()  
            return result
        except Exception as e:
            session.rollback()  
            raise e
        finally:
            session.close() 
    return wrapper
