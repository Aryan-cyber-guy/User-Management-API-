from pydantic import BaseModel

# Create a Pydantic model for user data validation
class Users(BaseModel):
    uid :int
    name : str
    email : str
    password : str