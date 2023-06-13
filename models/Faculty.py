from pydantic import BaseModel

class Faculty(BaseModel):
    facultyEmail: str
    facultyName: str
    facultyImageURL: str
    facultyPhoneNumber: str
    department: str
    designation: str
    group: int
    invigilationHours: int