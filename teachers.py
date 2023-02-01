import json
from disciplines import Discipline
class Teacher:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.firstName = jsonDict["firstName"]
        self.lastName = jsonDict["lastName"]
        self.middleName = jsonDict["middleName"]
        self.discipline = Discipline(jsonDict["discipline"])
        self.isHeadTeacher = jsonDict["isHeadTeacher"]

# deserialization from json
def teachersList(jsonStr):
    teachersDictList = json.loads(jsonStr)
    buttonsList = []
    for teacherDict in teachersDictList:
        teacher = Teacher(teacherDict)
        buttonsList.append(str(teacher.firstName + " " + str(teacher.lastName)))
    return buttonsList

def teachersIds(jsonStr):
    teachersDictList = json.loads(jsonStr)
    teachersId = []
    for teacherDict in teachersDictList:
        teacher = Teacher(teacherDict)
        teachersId.append(str(teacher.id))
    return teachersId

def extractTeacherId(jsonStr):
    teachersDictList = json.loads(jsonStr)
    teacherId = ""
    for teacherDict in teachersDictList:
        teacher = Teacher(teacherDict)
        teacherId = teacher.id
    return teacherId