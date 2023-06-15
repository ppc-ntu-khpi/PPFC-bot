import json
from groups import Group
from teachers import Teacher

class Change:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.group = Group(jsonDict["group"])
        if "classroom" in jsonDict:
            self.classroom = Classroom(jsonDict["classroom"])
        else:
            self.classroom = None
        if "teacher" in jsonDict:
            self.teacher = Teacher(jsonDict["teacher"])
        else:
            self.teacher = None
        if "subject" in jsonDict:
            self.subject = Subject(jsonDict["subject"])
        else:  
            self.subject = None
        self.isSubject = jsonDict["isSubject"]
        if "lessonNumber" in jsonDict:
            self.lessonNumber = jsonDict["lessonNumber"]
        else:
            self.lessonNumber = None

        if "eventName" in jsonDict:
            self.event = jsonDict["eventName"]
        else:
            self.event = None
        self.date = jsonDict["date"]

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

def changeCreator(jsonStr, userGroup):
    changeDictList = json.loads(jsonStr)
    changes = {}
    events = {}

    for changeDict in changeDictList:
        change = Change(changeDict)
        date = change.date

        if change.subject is None:
            subject = None
        else:
            subject = change.subject.name

        lessonNumber = change.lessonNumber
        group = change.group.number

        if change.teacher is None:
            teacher = None
        else:
            teacher = change.teacher.firstName + " " + change.teacher.lastName

        if change.classroom is None:
            classroom = None
        else:
            classroom = change.classroom.name

        if change.event is None:
            event = None
        else:
            event = change.event

        dayNumber = change.dayNumber
        isNumerator = change.isNumerator
        if date not in changes:
            changes[date] = []

        changes[date].append((lessonNumber, subject, group, teacher, classroom, event, dayNumber, isNumerator))

        # Grouping by event
        if event is not None:
            if event not in events:
                events[event] = []
            events[event].append((group, lessonNumber, subject, teacher, classroom))
        
    changeForm = " "
    for date, change in changes.items():
        changeForm += "*Зміни на " + str(date) + formatNumberToDay(dayNumber) + formatIsNumerator(isNumerator) + "*\n"
        for lesson in change:

            if lesson[5] == None:
                symbol = " ➡️ "

                if userGroup == str(lesson[2]):
                    symbol = " ✅ "

                if str(lesson[4]) == "зал":
                    lessonEnding = ""
                else:
                    lessonEnding = " ауд."

                groupSegment = str(lesson[2]) + " група"

                if lesson[1] is None:
                    subjectSegment = ""
                else:
                    subjectSegment = symbol + str(lesson[1])

                if lesson[5] is None:
                    eventSegment = ""
                else:
                    eventSegment = symbol + str(lesson[5])

                if lesson[0] is None:
                    lessonNumSegment = ""
                else:
                    lessonNumSegment = symbol + str(lesson[0]) + " пара"

                if lesson[3] is None:
                    teacherSegment = ""
                else:
                    teacherSegment = symbol + str(lesson[3])

                if lesson[4] is None:
                    classroomSegment = ""
                else:
                    classroomSegment = symbol + str(lesson[4]) + lessonEnding

                changeForm += groupSegment + eventSegment + lessonNumSegment + subjectSegment + teacherSegment + classroomSegment + "\n"
            else: continue
    # Grouping by event
    eventForm = ""
    for event, event_lessons in events.items():
        groups = ", ".join(str(lesson[0]) for lesson in event_lessons)
        if userGroup in groups:
            eventForm += groups + " групи ✅ " + event + "\n"
        else:
            eventForm += groups + " групи ➡️ " + event + "\n"

    return changeForm + "\n" + eventForm



def formatNumberToDay(dayNumber):
    if dayNumber == 1:
        dayName = " (Понеділок: "
    if dayNumber == 2:
        dayName = " (Вівторок: "
    if dayNumber == 3:
        dayName = " (Середа: "
    if dayNumber == 4:
        dayName = " (Четвер:"
    if dayNumber == 5:
        dayName = " (П'ятниця: "
    return dayName

def formatIsNumerator(bool):
    state = ""
    if bool == True:
        state = "Чисельник) 🔵"
    if bool == False:
        state = "Знаменник) 🟡"
    return state

#Lesson0 = lessonNumber +
#lesson1 = subject +
#lesson2 = group
#lesson3 = teacher +
#lesson4 = classroom +
#lesson5 = event +