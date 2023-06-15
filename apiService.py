import requests
import json
import datetime
import os

from Constants import Constants

username = Constants.username
password = Constants.password

baseLink = Constants.baseLink

def authenticate():
    url = baseLink + '/authenticate'
    myobj = {
	"username": username,
	"password": password
    }
    x = requests.post(url, json = myobj)
    auth = json.loads(x.text)
    accToken = auth["accessToken"]
    #print(accToken)
    print("TOKEN GENERATED")
    headers = {'Authorization': "Bearer {}".format(accToken)}

    return headers

def checkUser(userID, headers):
    url = baseLink + "/user/{}".format(userID)
    x = requests.get(url, headers = headers)
    if x.status_code == 200:
        return True
    return False

def checkToken(headers):
    url = baseLink + '/course'
    x = requests.get(url, headers = headers)
    
    if x.status_code == 200:
        return True
    return False

def register(ParamString, headers, userID):

    url = baseLink + "/user"
    userData = ParamString

    if checkUser(userID, headers):
        x = requests.put(url, headers = headers, json = userData)
    else: 
        x = requests.post(url, headers = headers, json = userData)

def disciplinesApi(headers):
    url = baseLink + '/discipline'
    x = requests.get(url, headers = headers)
    disciplinesDict = x.text
    
    return disciplinesDict

def coursesApi(headers):
    url = baseLink + '/course'
    x = requests.get(url, headers = headers)
    coursesDict = x.text
    
    return coursesDict

def groupByCourse(headers, par):
    url = baseLink + '/group?courseId='+ str(par)
    x = requests.get(url, headers = headers)
    groupsFromCourseDict = x.text

    return groupsFromCourseDict
    
def teacherByDiscipline(headers, par):
    url = baseLink + '/teacher?disciplineName='+ par
    x = requests.get(url, headers = headers)
    teachersFromDisciplineDict = x.text
    return teachersFromDisciplineDict
    
def getUserById(userId, headers):
    if checkUser(userId, headers):
        url = baseLink + "/user/{}".format(userId)
        x = requests.get(url, headers = headers)
        userData = x.text
    return userData

def getUsers(headers):
    url = baseLink + "/user"
    x = requests.get(url, headers=headers)
    users = x.text
    return users

def getTeacherIdForUse(headers, par):
    url = baseLink + '/teacher/byFirstAndLastName/' + par
    x = requests.get(url, headers = headers)
    teacher = x.text
    
    return teacher

def getGroupByNumber(headers, par):
    url = baseLink + '/group/byNumber/' + par
    x = requests.get(url, headers = headers)
    group = x.text

    return group
    
def getGroupById(headers, par):
    url = baseLink + '/group/'+ str(par)
    x = requests.get(url, headers = headers)
    group = x.text

    return group

def getTeacherById(headers, par):
    url = baseLink + '/teacher/'+ str(par)
    x = requests.get(url, headers = headers)
    teacher = x.text

    return teacher

def getScheduleByGroup(headers, par):
    url = baseLink + '/schedule?groupId='+ str(par)
    x = requests.get(url, headers = headers)
    scheduleGroup = json.loads(x.text)
    sorted_data = sorted(scheduleGroup, key=lambda x: (x['dayNumber'], x['lessonNumber'], not x['isNumerator']))

    schedule = json.dumps(sorted_data)
    return schedule

def getScheduleByTeacher(headers, par):
    url = baseLink + '/schedule?teacherId='+ str(par)
    x = requests.get(url, headers = headers)
    scheduleTeacher = json.loads(x.text)
    sorted_data = sorted(scheduleTeacher, key=lambda x: (x['dayNumber'], x['lessonNumber'], not x['isNumerator']))

    schedule = json.dumps(sorted_data)
    return schedule

def getChanges(headers, date):
    url = baseLink + '/change?date='+ str(date)
    x = requests.get(url, headers = headers)
    changeForGroup = json.loads(x.text)

    change = json.dumps(changeForGroup)
    return change

def getScheduleForRegUser(headers, date, userData):
    url = baseLink + '/schedule?dayNumber='+ str(date) + str(userData)
    x = requests.get(url, headers = headers)
    changeForGroup = json.loads(x.text)
    sorted_data = sorted(changeForGroup, key=lambda x: x['lessonNumber'])

    change = json.dumps(sorted_data)
    return change
