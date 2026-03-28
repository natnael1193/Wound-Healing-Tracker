from app.db.dependency import get_db
import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import text
from app.routes.api.auth import router as auth_router
from app.routes.api.user import router as user_router

app = fastapi.FastAPI()


@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).fetchone()
    print(result)   
    return {"db_connection": result[0]}




# Import routes
app.include_router(auth_router)
app.include_router(user_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
