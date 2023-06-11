def courseEntity(course) -> dict:
    return {
        "id": str(course["_id"]),
        "courseName": course["courseName"],
        "courseCode": course["courseCode"],
        "department": course["department"],
        "description": course["description"],
        "credit": course["credit"],
    }

def coursesEntity(entity) -> list:
    return [courseEntity(course) for course in entity] 