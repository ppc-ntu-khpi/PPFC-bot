import json
from courses import Course

class Group:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.number = jsonDict["number"]
        self.course = Course(jsonDict["course"])

# deserialization from json
def groupsList(jsonStr):
    groupsDictList = json.loads(jsonStr)
    buttonsList = []
    for groupDict in groupsDictList:
        group = Group(groupDict)
        buttonsList.append(str(group.number))
    return buttonsList

def groupsIds(jsonStr):
    groupsDictList = json.loads(jsonStr)
    groupsId = []
    for groupDict in groupsDictList:
        group = Group(groupDict)
        groupsId.append(str(group.id))
    return groupsId