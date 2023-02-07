import json
from groups import Group
from teachers import Teacher

class Change:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.group = Group(jsonDict["group"])
        self.classroom = Classroom(jsonDict["classroom"])
        self.teacher = Teacher(jsonDict["teacher"])
        self.subject = Subject(jsonDict["subject"])
        self.isSubject = jsonDict["isSubject"]
        self.lessonNumber = jsonDict["lessonNumber"]
        self.date = jsonDict["date"]
        self.isNumerator = jsonDict["isNumerator"]

class Subject:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.name = jsonDict["name"]

class Classroom:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.name = jsonDict["name"]

def changeCreator(jsonStr):
    changeDictList = json.loads(jsonStr)
    changes = {}
    for changeDict in changeDictList:
        change = Change(changeDict)
        date = change.date
        subject = change.subject.name
        lessonNumber = change.lessonNumber
        group = change.group.number
        teacher = change.teacher.lastName + " " + change.teacher.firstName
        classroom = change.classroom.name

        if date not in changes:
            changes[date] = []

        changes[date].append((lessonNumber, subject, group, teacher, classroom))

    changeForm = " "
    for date, change in changes.items():
        changeForm += "Зміни на " + str(date) + "\n"
        for lesson in change:
            changeForm += str(lesson[0]) + ". "+ str(lesson[1]) + " ➡️ " + str(lesson[2]) + " група ➡️ " + str(lesson[3]) +  " ➡️ " + str(lesson[4]) + "ауд.\n"
    return changeForm
