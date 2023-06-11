from datetime import datetime, timedelta
import random

from config.db import database

from models.Admin import Admin
from models.Faculty import Faculty
from models.Course import Course
from models.Exam import Exam
from models.Test import Test

from schemas.Admin import adminsEntity
from schemas.Faculty import facultysEntity
from schemas.Course import coursesEntity
from schemas.Exam import examsEntity
from schemas.Test import testsEntity

IMAGE = "https://st3.depositphotos.com/1011434/13157/i/600/depositphotos_131572502-stock-photo-happy-woman-smiling.jpg"

departments = ["ABC","DEF","XYZ"]

#ADMIN
def seed_admin(admin_count: int):
    names = []
    for i in range(1, admin_count+1):
        names.append(f"TestAdmin{i}")
    data = []
    for name in names:
        item: Admin = {
            "adminName": name,
            "adminEmail": (f"{name}@gmail.com"),
            "adminImageURL": IMAGE,
            "adminPhoneNumber": "1234567890",
        }
        data.append(item)
    database["admin"].insert_many(data)
    return adminsEntity(database["admin"].find())

def seed_faculty(faculty_count: int):
    names = []
    for i in range(1, faculty_count+1):
        names.append(f"TestFaculty{i}")
    data = []
    for name in names:
        department = random.sample(departments, 1)[0]
        item: Faculty = {
            "facultyName": name,
            "facultyEmail": (f"{name}@gmail.com"),
            "facultyImageURL": IMAGE,
            "facultyPhoneNumber": "1234567890",
            "department": department,
            "group": 1,
            "designation": "Professor",
        }
        data.append(item)
    database["faculty"].insert_many(data)
    return facultysEntity(database["faculty"].find())

def seed_course(course_count):
    names = []
    for i in range(1, course_count+1):
        names.append(f"TestCourse{i}")
    data = []
    for name in names:
        department = random.sample(departments, 1)[0]
        item: Course = {
            "courseName": name,
            "courseCode": (f"{name}123"),
            "department": department,
            "description": "A random course description",
            "credit": random.randint(2,4),
        }
        data.append(item)
    database["course"].insert_many(data)
    return coursesEntity(database["course"].find())

def seed_exam(exam_count):
    names = []
    for i in range(1, exam_count+1):
        names.append(f"TestExam{i}")
    data = []

    admins = adminsEntity(database["admin"].find())

    if len(admins) == 0:
        return []

    for name in names:
        department = random.sample(departments, 1)[0]

        startDate = datetime.now() + timedelta(random.randint(7,14))
        endDate = startDate + timedelta(random.randint(4,7))
        deadline = startDate - timedelta(random.randint(2,4))
        
        courses = coursesEntity(database["course"].find(filter={
            "department": department
        }))
        
        faculties = facultysEntity(database["faculty"].find(filter={
            "department": department
        }))

        item: Exam = {
            "examName": name,
            "department": "ABC",
            "description": "A random course description",
            "startDate": startDate,
            "endDate": endDate,
            "isFinalised": True if random.randint(0,1) == 1 else False,
            "numberOfCourses": random.randint(0, len(courses)),
            "deadline": deadline,
            "numberOfResponses": random.randint(0,len(faculties)),
            "createdBy": admins[random.randint(0,len(admins)-1)]["id"],
            "group": 1
        }
        data.append(item)
    database["exam"].insert_many(data)
    return examsEntity(database["exam"].find())


def seed_test():
    exams = examsEntity(database["exam"].find())
    for exam in exams:
        department = exam["department"]
        group = exam["group"]
        test_count = exam["numberOfCourses"]
        courses = coursesEntity(database["course"].find(filter={
            "department": department
        }))
        courses = random.sample(courses, min(len(courses), test_count))
        faculties = facultysEntity(database["faculty"].find(filter={
            "department": department,
            "group": group,
        }))
        if len(faculties) == 0:
            break
        data = []
        for course in courses:
            requiredFaculties = random.randint(1, len(faculties))
            signedUpFaculties = [faculty["id"] for faculty in faculties] # everyone in the department signed up
            signedUpFaculties = random.sample(signedUpFaculties, random.randint(0,len(signedUpFaculties)-1))
            if exam["isFinalised"]:
                finalisedFaculties = random.sample(signedUpFaculties, min(len(signedUpFaculties), requiredFaculties))
            else:
                finalisedFaculties = []
            item: Test = {
                "examId": exam["id"],
                "courseId": course["id"],
                "date": exam["startDate"],
                "time": datetime.now(),
                "requiredFaculties": requiredFaculties,
                "signedUpFaculties":  signedUpFaculties,
                "finalisedFaculties": finalisedFaculties,
            }
            data.append(item)
        if len(data):
            database["test"].insert_many(data)
    return testsEntity(database["test"].find())

def seed(collection=None):
    if collection == "admin":
        seed_admin(2)
    elif collection == "faculty":
        seed_faculty(5)
    elif collection == "course":
        seed_course(5)
    elif collection == "exam":
        seed_exam(5)
    elif collection == "test":
        seed_test()
    else:
        count = 10
        seed_admin(count)
        seed_faculty(count*3)
        seed_course(count*2)
        seed_exam(count)
        seed_test()

def delete_all(collection = None):
    if collection:
        ids = []
        data = database[collection].find()
        for record in data:
            ids.append(record["_id"])
        for id in ids:
            database[collection].find_one_and_delete({"_id": id})
    else:
        collections = ["admin", "faculty", "course", "exam", "test"]
        for collection in collections:
            ids = []
            data = database[collection].find()
            for record in data:
                ids.append(record["_id"])
            for id in ids:
                database[collection].find_one_and_delete({"_id": id})
            