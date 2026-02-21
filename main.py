from fastapi import FastAPI, Depends
from models import Users
from database import session,engine
from db_models import Db_users, base
from sqlalchemy.orm import Session
from fastapi import HTTPException

app = FastAPI()

# Create a db session and closes it after using
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# Create all tables with base class
base.metadata.create_all(bind=engine)

# Hello message for testing api
@app.get("/")
def greet():
    return {"message":"It's working"}

# Get a specific user
@app.get("/users/{uid}")
def get_user(uid: int, db : Session = Depends(get_db)):
    user = db.query(Db_users).filter(Db_users.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

# Create and add user data
@app.post("/users")
def add_user(user: Users, db : Session = Depends(get_db)):
    new_user = Db_users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update a user data
@app.put("/users/{uid}")
def update_user(uid: int,password: str, user: Users, db : Session = Depends(get_db)):
    db_user = db.query(Db_users).filter(Db_users.uid == uid, Db_users.password == password).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="User ID or Password is wrong")
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user data
@app.delete("/users/{uid}")
def delete_user(uid: int, password: str, db: Session = Depends(get_db)):
    db_user = db.query(Db_users).filter(Db_users.uid == uid, Db_users.password == password).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="User ID or Password is wrong")
    db.delete(db_user)
    db.commit()
    return {"message":"Successfully deleted"}