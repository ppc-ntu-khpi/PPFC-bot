import datetime
from datetime import date
from time import sleep
from tokenize import group
from telebot import TeleBot
from buttons import *
from change import changeCreator
from courses import coursesList
from groups import extractGroupId, groupsList
from disciplines import disciplinesList
from common.Constants import Constants
from groups import groupsList
import markup as botMarkup
from apiService import *
from schedule import formatDayToNumber, scheduleCreator
from teachers import *
from users import *
import sched, time

today = date.today()
tomorrow = date.today() + datetime.timedelta(days=1)

print("Today: "+str(today))
print("Next day: "+str(tomorrow))


tag: str = "BOT"
headers = authenticate()
tbot = TeleBot(Constants.botToken)

сoursesButtonsNames = coursesList(coursesApi(headers))
groupsButtonNames = []
teacherButtonNames = []
disciplinesButtonsNames = disciplinesList(disciplinesApi(headers))

#тут був стакан

def recreacteHeaders(scheduler): 

    global headers

    scheduler.enter(3300, 1, recreacteHeaders, (scheduler,))
    headers = authenticate()



@tbot.message_handler(commands=["start"])
def start(message):

    userId = message.from_user.id
    if checkUser(userId, headers):
        markup = botMarkup.mainMenuMarkup()
        print("/start: user already exists")
        tbot.send_message(chat_id=message.chat.id, text = "Ми вас вже знаємо!", reply_markup=markup)

    else: 
        replyMessage = "Зареєструйтеся. Оберіть хто ви:"
        print("/start: user registration")
        markup = botMarkup.registerMarkup()
        tbot.send_message(chat_id=message.chat.id, text=replyMessage, reply_markup=markup)


@tbot.message_handler(commands=["change"])
def start(message):

    userId = message.from_user.id
    if checkUser(userId, headers):
        markup = botMarkup.registerMarkup()
        print("/change: users new data ")
        tbot.send_message(chat_id=message.chat.id, text = "Режим зміни користувача. Оберіть хто ви:", reply_markup=markup)
    else: 
        replyMessage = "Неможливо змінити, так як ви у нас вперше. Оберіть хто ви:"
        print("/change: user does not exists")
        markup = botMarkup.registerMarkup()
        tbot.send_message(chat_id=message.chat.id, text=replyMessage, reply_markup=markup)


@tbot.message_handler(content_types = "text")
def messageListener(message):
    global coursesButtonsNames
    global groupsButtonNames
    global disciplinesButtonsNames
    global teacherButtonNames

    if message.text ==  Register.TEACHER.value:
        registerAsTeacher(headers, message)
        tbot.register_next_step_handler(message, getTeachersNames, headers)
        

    if message.text ==  Register.STUDENT.value:
        registerAsStudent(headers, message)
        tbot.register_next_step_handler(message, getGroupsNumbers, headers)


    if message.text == MainMenuButtons.SCHEDULE_TODAY.value:
        todayDate = date.today().weekday() + 1
        userId = message.from_user.id
        userData = checkUserPerson(headers,userId)
        schedule = getScheduleForRegUser(headers, todayDate, userData)
        
        print("Schedule for today")
        scheduleForm = scheduleCreator(schedule)
        if scheduleForm == " ":
            scheduleForm = "Розклад відсутній"
        tbot.send_message(chat_id=message.chat.id, text= scheduleForm)
    
    if message.text == MainMenuButtons.SCHEDULE_TOMORROW.value:
        todayDate = date.today().weekday() + 2
        if todayDate > 5:
            todayDate = 1
        userId = message.from_user.id
        userData = checkUserPerson(headers,userId)
        schedule = getScheduleForRegUser(headers, todayDate, userData)
        
        print("Schedule for tomorrow")
        scheduleForm = scheduleCreator(schedule)
        if scheduleForm == " ":
            scheduleForm = "Розклад відсутній"
        tbot.send_message(chat_id=message.chat.id, text= scheduleForm)


    if message.text == MainMenuButtons.CHANGES_TODAY.value:
        todayDate = date.today()
        userId = message.from_user.id
        userData = checkUserPerson(headers,userId)
        change = getChangesForRegUser(headers, todayDate, userData)

        print("Changes for today")
        changes = changeCreator(change)
        if changes == " ":
            changes = "Змін немає"
        tbot.send_message(chat_id=message.chat.id, text= changes)


    if message.text == MainMenuButtons.CHANGES_TOMORROW.value:
        tomorrowDate = date.today() + datetime.timedelta(days=1)
        userId = message.from_user.id
        userData = checkUserPerson(headers,userId)
        change = getChangesForRegUser(headers, tomorrowDate, userData)

        print("Changes for tomorrow")
        changes = changeCreator(change)
        if changes == " ":
            changes = "Змін немає"
        tbot.send_message(chat_id=message.chat.id, text= changes)
    
    
    if message.text ==  MainMenuButtons.FIND_BY_TEACHER.value:
        userId= message.from_user.id

        disciplines = disciplinesApi(headers)
        disciplinesButtonsNames = disciplinesList(disciplines)
        print("Find by teacher: discipline")
            
        markup = botMarkup.tripleMarkup(disciplinesButtonsNames)
        tbot.send_message(chat_id=message.chat.id, text= "Виберіть дисципліну викладача:", reply_markup=markup)
        tbot.register_next_step_handler(message, showTeachers, headers)

        
    if message.text ==  MainMenuButtons.FIND_BY_GROUP.value:
        userId = message.from_user.id

        courses = coursesApi(headers)
        coursesButtonsNames = coursesList(courses)
        print("Find by group: course")
            
        markup = botMarkup.doubleMarkup(coursesButtonsNames)
        tbot.send_message(chat_id=message.chat.id, text= "Оберіть курс групи:", reply_markup=markup)
        tbot.register_next_step_handler(message, showGroups, headers)

        return

    if message.text == MainMenuButtons.FIND_BY_DAY.value:
        markup = botMarkup.findByDayWMarkup()
        print("Find by day: day")
        tbot.send_message(chat_id=message.chat.id, text="Оберіть день тижня", reply_markup=markup)
        tbot.register_next_step_handler(message, scheduleByDay, headers, )



    if message.text == MainMenuButtons.MAIN_MENU.value:
        markup = botMarkup.mainMenuMarkup()
        print("Main menu")
        tbot.send_message(chat_id=message.chat.id, text="Повертаємося у головне меню", reply_markup=markup)

        return

        #userData.id = id of teacher or group, userData.isStudent = true or false
        #userData = getUserId(getUserById(userId, headers))


# Main menu Functions
def scheduleByDay(message, headers):
    userId= message.from_user.id
    userData = checkUserPerson(headers,userId)

    dayNumber = formatDayToNumber(message)
    schedule = getScheduleForRegUser(headers, dayNumber, userData)

    print("Find by date: done")
    scheduleForm = scheduleCreator(schedule)
    if scheduleForm == " ":
            scheduleForm = "Розклад відсутній"
    tbot.send_message(chat_id=message.chat.id, text= scheduleForm)


def finalTeacherSearch(message, headers, par):
    par = message.text

    teacherData = getTeacherIdForUse(headers, par)
    teacherId = extractTeacherId(teacherData)
    print("Find by teacher: done")

    par = teacherId

    schedule = getScheduleByTeacher(headers,par)
    formatedSchedule = scheduleCreator(schedule)
    tbot.send_message(chat_id=message.chat.id, text= formatedSchedule)
    

def finalGroupSearch(message, headers, par):
    par = message.text
    groupData = getGroupIdForUse(headers, par)
    groupId = extractGroupId(groupData)
    print("Find by group: done")

    par = groupId

    schedule = getScheduleByGroup(headers,par)
    formatedSchedule = scheduleCreator(schedule)
    tbot.send_message(chat_id=message.chat.id, text= formatedSchedule)

def showGroups(message, headers):
    par = message.text

    groupsByCourse = groupByCourse(headers, par)
    groupsButtonNames = groupsList(groupsByCourse)
    print("Find by group: group")

    markup = botMarkup.fiveMarkup(groupsButtonNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть групу:", reply_markup=markup)
    tbot.register_next_step_handler(message, finalGroupSearch, headers, par)
    return

def showTeachers(message, headers):
    par = message.text

    teachersByDiscipline = teacherByDiscipline(headers, par)
    teacherButtonNames = teachersList(teachersByDiscipline)
    print("Find by teacher: teacher")

    markup = botMarkup.tripleMarkup(teacherButtonNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть викладача:", reply_markup=markup)
    tbot.register_next_step_handler(message, finalTeacherSearch, headers, par)
    return



#REGISTER
def registerAsTeacher(headers,message):
    
    disciplines = disciplinesApi(headers)
    disciplinesButtonsNames = disciplinesList(disciplines)
    print("Register as teacher: discipline")

    markup = botMarkup.tripleRegMarkup(disciplinesButtonsNames)
    tbot.send_message(chat_id=message.chat.id, text= "Виберіть вашу дисципліну:", reply_markup=markup)

    
    

def registerAsStudent(headers,message):

    courses = coursesApi(headers)
    coursesButtonsNames = coursesList(courses)
    print("Register as student: course")
        
    markup = botMarkup.doubleRegMarkup(coursesButtonsNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть курс вашої групи:", reply_markup=markup)



def getTeachersNames(message, headers):
    par = message.text
    teachersByDiscipline = teacherByDiscipline(headers, par)
    teacherButtonNames = teachersList(teachersByDiscipline)
    print("Register as teacher: teacher")

    markup = botMarkup.tripleRegMarkup(teacherButtonNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть себе:", reply_markup=markup)

    tbot.register_next_step_handler(message, getRegTeacherId, headers)
    
    
def getGroupsNumbers(message, headers):
    par = message.text

    groupsByCourse = groupByCourse(headers, par)
    groupsButtonNames = groupsList(groupsByCourse)
    print("Register as group: group")

    markup = botMarkup.fiveRegMarkup(groupsButtonNames)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть групу:", reply_markup=markup)
    tbot.register_next_step_handler(message, getRegGroupId, headers)



def getRegTeacherId(message, headers):
    par = message.text
    teacherData = getTeacherIdForUse(headers, par)
    teacherId = extractTeacherId(teacherData)
    print("Register as teacher: done")

    userId = message.from_user.id
    
    userData = {
	"id": "{}".format(userId),
	"teacherId":"{}".format(teacherId)
    }

    register(userData, headers, userId)
    markup = botMarkup.mainMenuMarkup()
    userData = getUserId(getUserById(userId, headers))

    tbot.send_message(chat_id=message.chat.id, text = "Ви зареєструвалися, індекс викладача {}".format(userData.id), reply_markup=markup)


def getRegGroupId(message, headers):
    par = message.text
    groupData = getGroupIdForUse(headers, par)
    groupId = extractGroupId(groupData)

    print("Register as student: done")

    userId = message.from_user.id

    userData = {
	"id": "{}".format(userId),
	"groupId":"{}".format(groupId)
    }
    register(userData, headers, userId)
    markup = botMarkup.mainMenuMarkup()
    userData = getUserId(getUserById(userId, headers))
            
    tbot.send_message(chat_id=message.chat.id, text = "Ви зареєструвалися, індекс групи {}".format(userData.id), reply_markup=markup)


def main():
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(3300, 1, recreacteHeaders, (my_scheduler,))
    my_scheduler.run()

    tbot.infinity_polling()
    
if __name__ == "__main__":
    main()