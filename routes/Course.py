from fastapi import APIRouter

from models.Course import Course
from config.db import database

from schemas.Course import courseEntity, coursesEntity

from typing import Union
from bson import ObjectId

COLLECTION_NAME = "course"

course = APIRouter()

#CREATE
@course.post('/')
async def create_course(course: Course):
    document = database[COLLECTION_NAME].insert_one(dict(course))
    return courseEntity(database[COLLECTION_NAME].find_one({"_id":document.inserted_id}))

# READ
@course.get('/')
async def get_course(courseID: Union[str, None] = None):
    if courseID:
        document = database[COLLECTION_NAME].find_one({"_id": ObjectId(courseID)})
        if document:
            return courseEntity(document)
        else:
            return {}
    return coursesEntity(database[COLLECTION_NAME].find())

#UPDATE
@course.put('/{courseID}')
async def update_course(courseID, course: Course):
    database[COLLECTION_NAME].find_one_and_update({"_id": ObjectId(courseID)},{
        "$set": dict(course)
    })
    document = database[COLLECTION_NAME].find_one({"_id": ObjectId(courseID)})
    return courseEntity(document)

#DELETE
@course.delete('/{courseID}')
async def delete_course(courseID):
    document = database[COLLECTION_NAME].find_one_and_delete({"_id": ObjectId(courseID)})
    if document:
        return courseEntity(document)
    else:
        return {}