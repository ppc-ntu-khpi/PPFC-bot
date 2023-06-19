#-----------------------------------------
#-  Copyright (c) 2023. Lazovikov Illia  -
#-----------------------------------------

import json

class Discipline:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.name = jsonDict["name"]

# deserialization from json
def disciplinesList(jsonStr):
    disciplinesDictList = json.loads(jsonStr)
    buttonsList = []
    for disciplineDict in disciplinesDictList:
        discipline = Discipline(disciplineDict)
        buttonsList.append(str(discipline.name))
    return buttonsList
    
    