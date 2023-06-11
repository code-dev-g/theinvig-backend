def testEntity(test) -> dict:
    return {
        "id": str(test["_id"]),
        "examId": test["examId"],
        "courseId": test["courseId"],
        "date": test["date"],
        "time": test["time"],
        "requiredFaculties": test["requiredFaculties"],
        "signedUpFaculties": test["signedUpFaculties"],
        "finalisedFaculties": test["finalisedFaculties"],
    }

def testsEntity(entity) -> list:
    return [testEntity(test) for test in entity] 