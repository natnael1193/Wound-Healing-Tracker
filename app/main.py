from db.dependency import get_db
import fastapi
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import text


app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).fetchone()
    print(result)   
    return {"db_connection": result[0]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
