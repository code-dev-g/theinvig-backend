from fastapi import APIRouter

from bson import ObjectId

from config.db import database

from schemas.Exam import examEntity
from schemas.Test import testEntity, testsEntity
from schemas.Faculty import facultysEntity, facultyEntity

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

@custom.get('/finalize_faculties/{examId}')
async def finalize_faculties(examId):
    try:
        examId = ObjectId(examId)
        tests = testsEntity(database["test"].find(filter={
            "examId": examId
        }))
        for test in tests:
            facultyIds = test["signedUpFaculties"]
            hoursCount = dict()
            for facultyId in facultyIds:
                faculty = facultyEntity(database['faculty'].find_one(filter={
                    "_id": facultyId
                }))
                invigilationHours = faculty["invigilationHours"]
                hoursCount[facultyId] = invigilationHours
            sortedHours = sorted(hoursCount.items(), key=lambda x:x[1])
            finalFaculties = sortedHours[:test["requiredFaculties"]]
            finalFaculties = [i[0] for i in finalFaculties]
            test["finalisedFaculties"] = finalFaculties
            updatedTest = testEntity(database['test'].find_one_and_update(filter={
                "_id": test["id"]
            }, update={
                "$set": dict(test)
            }))
            for facultyId in finalFaculties:
                faculty = facultyEntity(database['faculty'].find_one(filter={
                    "_id": facultyId
                }))
                faculty["invigilationHours"] += 1
                updatedFaculty = facultyEntity(database["faculty"].find_one_and_update(filter={"_id": facultyId}, update={
                    "$set": dict(faculty)
                }))
        return "Success"
    except:
        return "Failed"
    
