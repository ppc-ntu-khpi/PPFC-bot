from apiService import coursesApi, disciplinesApi, groupByCourse, teacherByDiscipline
from courses import coursesList
from disciplines import disciplinesList
from groups import groupsIds, groupsList
import markup as botMarkup
from telebot import TeleBot
from common.Constants import Constants
from teachers import teachersIds, teachersList


tbot = TeleBot(Constants.botToken)
coursesButtonsNames = []
disciplinesButtonsNames = []
teacherButtonsNames = []
groupsButtonNames = []

def registerAsTeacher(headers,message):
    
    global disciplinesButtonsNames
    
    disciplines = disciplinesApi(headers)
    disciplinesButtonsNames = disciplinesList(disciplines)
    print("Register as teacher: discipline")

    markup = botMarkup.tripleRegMarkup(disciplinesButtonsNames)
    tbot.send_message(chat_id=message.chat.id, text= "Виберіть вашу дисципліну:", reply_markup=markup)
    

def registerAsStudent(headers,message):

    global coursesButtonsNames

    courses = coursesApi(headers)
    coursesButtonsNames = coursesList(courses)
    print("Register as student: course")
        
    markup = botMarkup.doubleRegMarkup(coursesButtonsNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть курс вашої групи:", reply_markup=markup)


    

def teacherGetNames(message, headers):

    global disciplinesButtonsNames
    global teachersButtonNames
    
    par = message.text
    teachersByDiscipline = teacherByDiscipline(headers, par)
    teachersButtonNames = teachersList(teachersByDiscipline)
    print("Register as teacher: teacher")

    markup = botMarkup.tripleRegMarkup(teachersButtonNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть себе:", reply_markup=markup)
    

    return par

def teacherRegID(message,headers, par):

    global teachersButtonsNames

    teachersId = teachersIds(teacherByDiscipline(headers,par))
    teacherName = message.text  

    index = teachersButtonNames.index(teacherName)
    teacherRegId = teachersId[index]

    return teacherRegId

def groupGetNames(message, headers):

    global coursesButtonsNames
    global groupsButtonNames
    
    par = message.text

    groupsByCourse = groupByCourse(headers, par)
    groupsButtonNames = groupsList(groupsByCourse)
    print("Register as student: group")

    markup = botMarkup.fiveRegMarkup(groupsButtonNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть вашу групу:", reply_markup=markup)

    return par
def groupRegID(message, headers, par):
    
    global groupsButtonNames

    groupsId = groupsIds(groupByCourse(headers,par))
    groupNumber = message.text

    index = groupsButtonNames.index(groupNumber)
    studentRegId = groupsId[index]

    return studentRegId