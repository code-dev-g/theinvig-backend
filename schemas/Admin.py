def adminEntity(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "adminName": admin["adminName"],
        "adminEmail": admin["adminEmail"],
        "adminImageURL": admin["adminImageURL"],
        "adminPhoneNumber": admin["adminPhoneNumber"],
    }

def adminsEntity(entity) -> list:
    return [adminEntity(admin) for admin in entity] 