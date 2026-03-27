
from session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        result = db.execute("SELECT 1").fetchone()
        print("DB connection successful:", result[0])
        # yield db
    finally:
        print("Database connection closed")
        db.close()