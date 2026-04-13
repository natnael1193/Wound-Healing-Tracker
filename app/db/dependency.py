
from app.db.session import SessionLocal
from sqlalchemy import text

def get_db():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print("DB connection successful:", result[0])
        yield db
    finally:
        print("Database connection closed")
        db.close()