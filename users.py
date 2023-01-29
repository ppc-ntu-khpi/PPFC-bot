import json
from groups import Group
from teachers import Teacher

class User:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.teacher = jsonDict.get("teacher")
        self.group = jsonDict.get("group")
        self.isGroup = jsonDict["isGroup"]
        
class UserId:
    def __init__(self, id, isStudent):
        self.id = id
        self.isStudent = isStudent
        
def getUserId(jsonStr):
    userDict = json.loads(jsonStr)
    user = User(userDict)
    
    if(user.isGroup):
        group = Group(user.group)
        if(group is None):
            return None
        
        return UserId(group.id, user.isGroup)
    else:
        teacher = Teacher(user.teacher)
        if(teacher is None):
            return None
            
        return UserId(teacher.id, user.isGroup)