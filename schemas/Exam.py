def examEntity(exam) -> dict:
    return {
        "id": str(exam["_id"]),
        "examName": exam["examName"],
        "department": exam["department"],
        "description": exam["description"],
        "startDate": exam["startDate"],
        "endDate": exam["endDate"],
        "createdBy": exam["createdBy"],
        "isFinalised": exam["isFinalised"],
        "numberOfCourses": exam["numberOfCourses"],
        "numberOfResponses": exam["numberOfResponses"],
        "deadline": exam["deadline"],
        "group": exam["group"],
    }

def examsEntity(entity) -> list:
    return [examEntity(exam) for exam in entity] 