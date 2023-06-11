from fastapi import APIRouter

from bson import ObjectId

from config.db import database

from schemas.Exam import examEntity
from schemas.Test import testEntity

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