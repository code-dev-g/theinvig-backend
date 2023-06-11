from pydantic import BaseModel

class Admin(BaseModel):
    adminEmail: str
    adminName: str
    adminImageURL: str
    adminPhoneNumber: str