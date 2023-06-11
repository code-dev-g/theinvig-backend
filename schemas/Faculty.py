def facultyEntity(faculty) -> dict:
    return {
        "id": str(faculty["_id"]),
        "facultyName": faculty["facultyName"],
        "facultyEmail": faculty["facultyEmail"],
        "facultyImageURL": faculty["facultyImageURL"],
        "facultyPhoneNumber": faculty["facultyPhoneNumber"],
        "department": faculty["department"],
        "designation": faculty["designation"],
        "groups": faculty["groups"],
    }

def facultysEntity(entity) -> list:
    return [facultyEntity(faculty) for faculty in entity] 