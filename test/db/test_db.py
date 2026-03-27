
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from db.session import SessionLocal


try:
    db = SessionLocal()
    print("DB connection successful")
finally:
    db.close()