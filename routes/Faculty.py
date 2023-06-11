from fastapi import APIRouter

from models.Faculty import Faculty
from config.db import database

from schemas.Faculty import facultyEntity, facultysEntity

from typing import Union

COLLECTION_NAME = "faculty"

faculty = APIRouter()

#CREATE
@faculty.post('/')
async def create_faculty(faculty: Faculty):
    document = database[COLLECTION_NAME].insert_one(dict(faculty))
    return facultysEntity(database[COLLECTION_NAME].find_one({"_id":document.inserted_id}))

# READ
@faculty.get('/')
async def get_faculty(facultyEmail: Union[str, None] = None):
    if facultyEmail:
        document = database[COLLECTION_NAME].find_one({"facultyEmail": facultyEmail})
        if document:
            return facultyEntity(document)
        else:
            return {}
    return facultysEntity(database[COLLECTION_NAME].find())

#UPDATE
@faculty.put('/{facultyemail}')
async def update_faculty(facultyemail, faculty: Faculty):
    database[COLLECTION_NAME].find_one_and_update({"facultyEmail": facultyemail},{
        "$set": dict(faculty)
    })
    document = database[COLLECTION_NAME].find_one({"facultyEmail": facultyemail})
    return facultyEntity(document)

#DELETE
@faculty.delete('/{facultyemail}')
async def delete_faculty(facultyemail):
    document = await database[COLLECTION_NAME].find_one_and_delete({"facultyEmail": facultyemail})
    if document:
        return facultyEntity(document)
    else:
        return {}