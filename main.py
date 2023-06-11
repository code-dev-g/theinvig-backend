from fastapi import FastAPI

from config.seed import seed, delete_all

from routes.Admin import admin
from routes.Faculty import faculty
from routes.Course import course
from routes.Exam import exam
from routes.Test import test

app = FastAPI()

# delete_all()
# seed()

app.include_router(admin, prefix='/admin', tags=["Admin"])
app.include_router(faculty, prefix='/faculty', tags=["Faculty"])
app.include_router(course, prefix='/course', tags=["Course"])
app.include_router(exam, prefix='/exam', tags=["Exam"])
app.include_router(test, prefix='/test', tags=["Test"])

@app.get("/")
async def root():
    return {
        "title": "TheINVIG",
        "desc": "Invigilation management system"
        }