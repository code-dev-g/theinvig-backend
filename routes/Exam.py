from fastapi import APIRouter

from models.Exam import Exam
from config.db import database

from schemas.Exam import examEntity, examsEntity

from typing import Union
from bson import ObjectId

COLLECTION_NAME = "exam"

exam = APIRouter()

#CREATE
@exam.post('/')
async def create_exam(exam: Exam):
    document = database[COLLECTION_NAME].insert_one(dict(exam))
    return examEntity(database[COLLECTION_NAME].find_one({"_id":document.inserted_id}))

# READ
@exam.get('/')
async def get_exam(examID: Union[str, None] = None):
    if examID:
        document = database[COLLECTION_NAME].find_one({"_id": ObjectId(examID)})
        if document:
            return examEntity(document)
        else:
            return {}
    return examsEntity(database[COLLECTION_NAME].find())

#UPDATE
@exam.put('/{examID}')
async def update_exam(examID, exam: Exam):
    database[COLLECTION_NAME].find_one_and_update({"_id": ObjectId(examID)},{
        "$set": dict(exam)
    })
    document = database[COLLECTION_NAME].find_one({"_id": ObjectId(examID)})
    return examEntity(document)

#DELETE
@exam.delete('/{examID}')
async def delete_exam(examID):
    document = database[COLLECTION_NAME].find_one_and_delete({"_id": ObjectId(examID)})
    if document:
        return examEntity(document)
    else:
        return {}