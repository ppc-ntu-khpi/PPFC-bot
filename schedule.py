import json
from groups import Group
from teachers import Teacher

class Schedule:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.group = Group(jsonDict["group"])
        self.classroom = Classroom(jsonDict["classroom"])
        self.teacher = Teacher(jsonDict["teacher"])
        self.subject = Subject(jsonDict["subject"])
        self.isSubject = jsonDict["isSubject"]
        self.lessonNumber = jsonDict["lessonNumber"]
        self.dayNumber = jsonDict["dayNumber"]
        self.isNumerator = jsonDict["isNumerator"]

class Subject:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.name = jsonDict["name"]

class Classroom:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.name = jsonDict["name"]

def scheduleCreator(jsonStr):
    scheduleDictList = json.loads(jsonStr)
    schedules = {}
    for scheduleDict in scheduleDictList:
        schedule = Schedule(scheduleDict)
        dayNumber = schedule.dayNumber
        lessonNumber = schedule.lessonNumber
        group = schedule.group.number
        teacher = schedule.teacher.firstName + " " + schedule.teacher.lastName 
        classroom = schedule.classroom.name

        if dayNumber not in schedules:
            schedules[dayNumber] = []

        schedules[dayNumber].append((lessonNumber, group, teacher, classroom))
    scheduleForm = " "
    for dayNumber, schedule in schedules.items():
        dayName = formatNumberToDay(dayNumber)
        scheduleForm += dayName + "\n"
        for lesson in schedule:
            scheduleForm += str(lesson[0]) + " пара ➡️ "+ str(lesson[1]) + " група ➡️ " + str(lesson[2]) + " ➡️ " + str(lesson[3]) + "ауд.\n"
    return scheduleForm

def formatNumberToDay(dayNumber):
    if dayNumber == 1:
        dayName = "Понеділок:"
    if dayNumber == 2:
        dayName = "Вівторок:"
    if dayNumber == 3:
        dayName = "Середа:"
    if dayNumber == 4:
        dayName = "Четвер:"
    if dayNumber == 5:
        dayName = "П'ятниця:"
    return dayName

def formatDayToNumber(message):
    dayNumber = ""
    if message.text == "Понеділок":
        dayNumber = 1
    if message.text == "Вівторок":
        dayNumber = 2
    if message.text == "Середа":
        dayNumber = 3
    if message.text == "Четвер":
        dayNumber = 4
    if message.text == "П'ятниця":
        dayNumber = 5
    return dayNumber