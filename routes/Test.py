from fastapi import APIRouter

from models.Test import Test
from config.db import database

from schemas.Test import testEntity, testsEntity

from typing import Union
from bson import ObjectId

COLLECTION_NAME = "test"

test = APIRouter()

#CREATE
@test.post('/')
async def create_test(test: Test):
    document = database[COLLECTION_NAME].insert_one(dict(test))
    return testEntity(database[COLLECTION_NAME].find_one({"_id":document.inserted_id}))

# READ
@test.get('/')
async def get_test(testID: Union[str, None] = None):
    if testID:
        document = database[COLLECTION_NAME].find_one({"_id": ObjectId(testID)})
        if document:
            return testEntity(document)
        else:
            return {}
    return testsEntity(database[COLLECTION_NAME].find())

#UPDATE
@test.put('/{testID}')
async def update_test(testID, test: Test):
    database[COLLECTION_NAME].find_one_and_update({"_id": ObjectId(testID)},{
        "$set": dict(test)
    })
    document = database[COLLECTION_NAME].find_one({"_id": ObjectId(testID)})
    return testEntity(document)

#DELETE
@test.delete('/{testID}')
async def delete_test(testID):
    document = database[COLLECTION_NAME].find_one_and_delete({"_id": ObjectId(testID)})
    if document:
        return testEntity(document)
    else:
        return {}
    
# READ
@test.get('/examid/{examid}')
async def get_test_under_exam(examid):

    document = database[COLLECTION_NAME].find({"examId": ObjectId(examid)})
    if document:
        return testsEntity(document)
    else:
        return {}