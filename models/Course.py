from pydantic import BaseModel

class Course(BaseModel):
    courseName: str
    courseCode: str
    department: str
    credit: int
    description: str