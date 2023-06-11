from fastapi import APIRouter

from models.Admin import Admin
from config.db import database

from schemas.Admin import adminEntity, adminsEntity

from typing import Union

COLLECTION_NAME = "admin"

admin = APIRouter()

#CREATE
@admin.post('/')
async def create_admin(admin: Admin):
    document = database[COLLECTION_NAME].insert_one(dict(admin))
    return adminsEntity(database[COLLECTION_NAME].find_one({"_id":document.inserted_id}))

# READ
@admin.get('/')
async def get_admin(adminEmail: Union[str, None] = None):
    if adminEmail:
        document = database[COLLECTION_NAME].find_one({"adminEmail": adminEmail})
        if document:
            return adminEntity(document)
        else:
            return {}
    return adminsEntity(database[COLLECTION_NAME].find())

#UPDATE
@admin.put('/{adminemail}')
async def update_admin(adminemail, admin: Admin):
    database[COLLECTION_NAME].find_one_and_update({"adminEmail": adminemail},{
        "$set": dict(admin)
    })
    document = database[COLLECTION_NAME].find_one({"adminEmail": adminemail})
    return adminEntity(document)

#DELETE
@admin.delete('/{adminemail}')
async def delete_admin(adminemail):
    document = database[COLLECTION_NAME].find_one_and_delete({"adminEmail": adminemail})
    if document:
        return adminEntity(document)
    else:
        return {}