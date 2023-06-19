#-----------------------------------------
#-  Copyright (c) 2023. Lazovikov Illia  -
#-----------------------------------------

import json

class Course:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.number = jsonDict["number"]

# deserialization from json
def coursesList(jsonStr):
    coursesDictList = json.loads(jsonStr)
    buttonsList = []
    for courseDict in coursesDictList:
        course = Course(courseDict)
        buttonsList.append(str(course.number))
    return buttonsList
    