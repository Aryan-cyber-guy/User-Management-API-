from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String

# Create a base class for the database models
base = declarative_base()

# Create a database model for users table
class Db_users(base):
    __tablename__ = "user_data"
    uid = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)