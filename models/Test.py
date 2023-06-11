from pydantic import BaseModel
import datetime

class Test(BaseModel):
    examId: str # exam ID
    courseId: str # course ID
    date: datetime.datetime
    time: datetime.datetime
    requiredFaculties: int
    signedUpFaculties: list
    finalisedFaculties: list