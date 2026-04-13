
from app.db.session import SessionLocal


try:
    db = SessionLocal()
    print("DB connection successful")
finally:
    db.close()