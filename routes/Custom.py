from fastapi import APIRouter

from bson import ObjectId

from config.db import database

from schemas.Exam import examEntity
from schemas.Test import testEntity
from schemas.Faculty import facultysEntity

from config.mailing import send_mail

custom = APIRouter()

@custom.post('/agree')
async def agree_for_test(testid, facultyid):
    document = database["test"].find_one(filter={
        "_id": ObjectId(testid)
    })

    if document:
        document = testEntity(document)
        examId = document["examId"]
        exam = examEntity(database["exam"].find_one({"_id": ObjectId(examId)}))
        if not exam["isFinalised"]:
            document["signedUpFaculties"].append(facultyid)
            newSignedUpFaculties = document["signedUpFaculties"]
            print(newSignedUpFaculties, document)
            database["test"].find_one_and_update(filter={
                    "_id": ObjectId(testid)
                },update={
                    "$set": dict(document),
                }
            )
        return testEntity(database["test"].find_one({"_id": ObjectId(testid)}))
    else:
        print("Here")
        {}

@custom.get("/addition_notif/{examid}")
async def send_exam_added_notification(examid):
    examid = ObjectId(examid)
    exam = database['exam'].find_one({"_id": examid})
    if exam:
        exam = examEntity(exam)
        group = exam["group"]

        faculties = database['faculty'].find(filter={
            "group": group
        })
        if faculties:
            faculties = facultysEntity(faculties)
            for faculty in faculties:
                email = faculty["facultyEmail"]
                subject = "THEINVIG - NEW EXAM ADDED"
                message = f"New exam, {exam['examName']} has been added to THEINVIG. Check it out to give your response."
                send_mail(email, subject, message)
        return "Success"
    return "Failed"

@custom.get("/final_notif/{examid}")
async def send_exam_finalised_notification(examid):
    examid = ObjectId(examid)
    exam = database['exam'].find_one({"_id": examid})
    if exam:
        exam = examEntity(exam)
        group = exam["group"]

        faculties = database['faculty'].find(filter={
            "group": group
        })

        if faculties:
            faculties = facultysEntity(faculties)
            for faculty in faculties:
                email = faculty["facultyEmail"]
                subject = "THEINVIG - SCHEDULE FINALISED"
                message = f"Schedule finalised, {exam['examName']}. Check it out to give your response."
                send_mail(email, subject, message)
        return "Success"
    return "Failed"


