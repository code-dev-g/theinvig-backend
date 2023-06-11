from pydantic import BaseModel
import datetime

class Exam(BaseModel):
    examName: str
    department: str
    startDate: datetime.datetime
    endDate: datetime.datetime
    createdBy: str # admin ID
    isFinalised: bool
    numberOfCourses: int
    numberOfResponses: int
    description: str
    deadline: datetime.datetime
    group: int