import datetime
from threading import Thread
from time import sleep
from tokenize import group
from telebot import TeleBot
from buttons import *
from change import changeCreator
from courses import coursesList
from groups import *
from disciplines import disciplinesList
from Constants import Constants
from groups import groupsList
import markup as botMarkup
from apiService import *
from schedule import *
from teachers import *
from users import *
import sched, time
import os



#--------------------- Date Control -------------------------------
def dayToday():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    return now

def dayTomorrow():
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(hours=2) + datetime.timedelta(days = 1)
    return tomorrow

today = dayToday()
tomorrow = dayTomorrow()

print("Today: "+str(today.strftime("%Y-%m-%d")))
print("Next day: "+str(tomorrow.strftime("%Y-%m-%d")))


# ----------------------------Chiselnik/Znamenik---------------------
def isCurrentWeekNumerator():
    dateNow = datetime.datetime.utcnow().replace(minute = 0, second = 0) + datetime.timedelta(hours = 2)

    dateSeptember = dateNow.replace(day=1, month=9)
    if dateNow.month < 9:
        dateSeptember -= datetime.timedelta(days=365.24)

    daysDifference = (dateNow - dateSeptember).days

    return not bool(int(daysDifference / 7) % 2) 

#----------------------- Message Control --------------------------
tag: str = "BOT"
headers = authenticate()
tbot = TeleBot(Constants.botToken)

сoursesButtonsNames = coursesList(coursesApi(headers))
groupsButtonNames = []
teacherButtonNames = []
disciplinesButtonsNames = disciplinesList(disciplinesApi(headers))

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
        markup = botMarkup.registerMarkup(userId, headers)
        tbot.send_message(chat_id=message.chat.id, text=replyMessage, reply_markup=markup)


@tbot.message_handler(commands=["change"])
def changeData(message):

    userId = message.from_user.id
    if checkUser(userId, headers):
        markup = botMarkup.registerMarkup(userId, headers)
        print("/change: users new data ")
        tbot.send_message(chat_id=message.chat.id, text = "Режим зміни користувача. Оберіть хто ви:", reply_markup=markup)
    else: 
        replyMessage = "Неможливо змінити, так як ви у нас вперше. Оберіть хто ви:"
        print("/change: user does not exists")
        markup = botMarkup.registerMarkup(userId, headers)
        tbot.send_message(chat_id=message.chat.id, text=replyMessage, reply_markup=markup)


@tbot.message_handler(content_types = "text")
def messageListener(message):
    global coursesButtonsNames
    global groupsButtonNames
    global disciplinesButtonsNames
    global teacherButtonNames

    userId = message.from_user.id

    if message.text ==  Register.TEACHER.value:
        registerAsTeacher(headers, message)
        tbot.register_next_step_handler(message, getTeachersNames, headers)
        

    if message.text ==  Register.STUDENT.value:
        registerAsStudent(headers, message)
        tbot.register_next_step_handler(message, getGroupsNumbers, headers)

    if message.text == MainMenuButtons.SCHEDULE_TODAY.value:
        if checkRegistration(message,headers):
            recreateToken(message,headers)
            todayDate = dayToday().weekday() + 1
            userId = message.from_user.id
            userData = checkUserPerson(headers,userId)
            schedule = getScheduleForRegUser(headers, todayDate, userData)
                
            print("Schedule for today")
            scheduleForm = scheduleCreator(schedule, isCurrentWeekNumerator())
            if scheduleForm == " ":
                scheduleForm = "Розклад відсутній"
            tbot.send_message(chat_id=message.chat.id, text= scheduleForm)
        
    if message.text == MainMenuButtons.SCHEDULE_TOMORROW.value:
        if checkRegistration(message,headers):
            recreateToken(message,headers)
            tomorrowDate = dayTomorrow().weekday() + 1
            if tomorrowDate > 5:
                tomorrowDate = 1
            userId = message.from_user.id
            userData = checkUserPerson(headers,userId)
            schedule = getScheduleForRegUser(headers, tomorrowDate, userData)
                
            print("Schedule for tomorrow")
            scheduleForm = scheduleCreator(schedule, isCurrentWeekNumerator())
            if scheduleForm == " ":
                scheduleForm = "Розклад відсутній"
            tbot.send_message(chat_id=message.chat.id, text= scheduleForm)


    if message.text == MainMenuButtons.CHANGES_TODAY.value:
        if checkRegistration(message,headers):
            recreateToken(message,headers)
            todayDate = dayToday().strftime("%Y-%m-%d")
            print(todayDate)
            userId = message.from_user.id
            userData = checkUserPerson(headers,userId)
            change = getChangesForRegUser(headers, todayDate, userData)

            print("Changes for today")
            changes = changeCreator(change)
            if changes == " ":
                    changes = "Змін немає"
            tbot.send_message(chat_id=message.chat.id, text= changes)


    if message.text == MainMenuButtons.CHANGES_TOMORROW.value:
        if checkRegistration(message,headers):
            recreateToken(message,headers)
            tomorrowDate = dayTomorrow().strftime("%Y-%m-%d")
            userId = message.from_user.id
            userData = checkUserPerson(headers,userId)
            change = getChangesForRegUser(headers, tomorrowDate, userData)

            print("Changes for tomorrow")
            changes = changeCreator(change)
            if changes == " ":
                changes = "Змін немає"
            tbot.send_message(chat_id=message.chat.id, text= changes)
        
        
    if message.text ==  MainMenuButtons.FIND_BY_TEACHER.value:
        if checkRegistration(message,headers):
            recreateToken(message,headers)
            userId= message.from_user.id

            disciplines = disciplinesApi(headers)
            disciplinesButtonsNames = disciplinesList(disciplines)
            print("Find by teacher: discipline")
                    
            markup = botMarkup.tripleMarkup(disciplinesButtonsNames)
            tbot.send_message(chat_id=message.chat.id, text= "Виберіть дисципліну викладача:", reply_markup=markup)
            tbot.register_next_step_handler(message, showTeachers, headers)

            
    if message.text ==  MainMenuButtons.FIND_BY_GROUP.value:
        if checkRegistration(message,headers):
            recreateToken(message,headers)
            userId = message.from_user.id

            courses = coursesApi(headers)
            coursesButtonsNames = coursesList(courses)
            print("Find by group: course")
                    
            markup = botMarkup.doubleMarkup(coursesButtonsNames)
            tbot.send_message(chat_id=message.chat.id, text= "Оберіть курс групи:", reply_markup=markup)
            tbot.register_next_step_handler(message, showGroups, headers)


    if message.text == MainMenuButtons.FIND_BY_DAY.value:
        if checkRegistration(message, headers):
            recreateToken(message,headers)
            markup = botMarkup.findByDayWMarkup()
            print("Find by day: day")
            tbot.send_message(chat_id=message.chat.id, text="Оберіть день тижня", reply_markup=markup)
            tbot.register_next_step_handler(message, scheduleByDay, headers)


    if message.text == MainMenuButtons.HELP.value:
        if checkRegistration(message, headers):
            recreateToken(message,headers)

            data = ""
            
            userData = getUserId(getUserById(userId, headers))
            if userData.isStudent == True:
                data = "Студент, " + str(extractGroupNumber(getGroupById(headers, userData.id))) + " група"
            if userData.isStudent == False:
                data = "Викладач, " + str(extractTeacherName(getTeacherById(headers, userData.id)))
            helpInstruction = 'Вітаємо у боті для ВСП ППФК НТУ "ХПІ"\n'
            helpInstruction += "\n"
            helpInstruction += "Для перезавантаження бота використайте команду /start\n\n"
            helpInstruction += "Для зміни ваших даних використайте команду /change\n"
            helpInstruction += "\n"
            helpInstruction += "Також ви можете переглянути усі додаткові функції натиснувши на відповідну кнопку у меню\n"
            helpInstruction += "Для скарг та пропозицій приєднуйтесь до чату: https://t.me/PPFC_BOT_Support\n"
            helpInstruction += "\n"
            helpInstruction += "Ваші реєстраційні дані: {}".format(data) 

            markup = botMarkup.mainMenuMarkup()
            print("Button Help")
            tbot.send_message(chat_id=message.chat.id, text=helpInstruction, reply_markup=markup)

    if message.text == MainMenuButtons.ADDITIONAL_FUNCTIONS.value:
        recreateToken(message,headers)
        if checkRegistration(message,headers):
            markup = botMarkup.additionalFuncMarkup()
    
            print("Additional functions")
            tbot.send_message(chat_id=message.chat.id, text= "Доступні додаткові функції", reply_markup=markup)

    if message.text == AdditionalFuncButtons.CHANGE_DATA:
        recreateToken(message,headers)
        if checkRegistration(message,headers):
            markup = botMarkup.mainMenuMarkup()
    
            print("Change data through additional functions")
            changeData(message)

    if message.text == AdditionalFuncButtons.WORK_SATURDAYS:
        recreateToken(message,headers)
        if checkRegistration(message,headers):
            
            print("Working saturdays")
            tbot.send_message(chat_id=message.chat.id, text= "Відсутні")

    if message.text == AdditionalFuncButtons.EDU_PROCESS:
        recreateToken(message,headers)
        if checkRegistration(message,headers):

            text = ""
            text += "Повний розклад поки що відсутній. \n"
            text += "Його буде додано пізніше у ході супроводу"

            print("Education Process Plan")
            tbot.send_message(chat_id=message.chat.id, text= text)
        
    if message.text == AdditionalFuncButtons.COLLEGE_MAP:
        recreateToken(message,headers)
        if checkRegistration(message,headers):
            markup = botMarkup.collegeMapMarkup()

            print("College map")
            tbot.send_message(chat_id=message.chat.id, text= "Виберіть поверх", reply_markup = markup)
            tbot.register_next_step_handler(message, showCollegeFloor)

    if message.text == AdditionalFuncButtons.RINGS_SCHEDULE:
        recreateToken(message,headers)
        if checkRegistration(message,headers):

            markup = botMarkup.mainMenuMarkup()
            
            print("Show ring schedule")
            imageName = "data/ringSchedule.png"
            tbot.send_photo(chat_id=message.chat.id, photo=open(imageName, 'rb'), reply_markup = markup)




    if MainMenuCheck(message):
        returnToMainMenu(message)
        return



#userData.id = id of teacher or group, userData.isStudent = true or false
#userData = getUserId(getUserById(userId, headers))

#------------------------------ Main check functions ---------------------------------
def checkRegistration(message, headers):
    userId = message.from_user.id
    if not checkUser(userId, headers):
        markup = botMarkup.mainMenuMarkup()
        tbot.send_message(chat_id=message.chat.id, text="Ви не зареєстровані. Для початку роботи виконайте команду /start",  reply_markup=markup)
        return False

    else: return True


def MainMenuCheck(message):
    if message.text == MainMenuButtons.MAIN_MENU.value:
        return True
    else: return False


def returnToMainMenu(message):
    markup = botMarkup.mainMenuMarkup()
    print("Main menu")
    tbot.send_message(chat_id=message.chat.id, text="Повертаємося у головне меню", reply_markup=markup)

def recreateToken(message, headers):
    userId = message.from_user.id
    if not checkUser(userId, headers):
        headers = authenticate()
    return
    
#--------------------------- Main menu Functions (Finders) -----------------------------
def scheduleByDay(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        userId= message.from_user.id
        userData = checkUserPerson(headers,userId)

        dayNumber = formatDayToNumber(message)
        schedule = getScheduleForRegUser(headers, dayNumber, userData)

        print("Find by date: done")
        
        markup = botMarkup.mainMenuMarkup()
        scheduleForm = scheduleCreator(schedule, None)
        if scheduleForm == " ":
                scheduleForm = "Розклад на цей день відсутній"
        tbot.send_message(chat_id=message.chat.id, text= scheduleForm, reply_markup=markup)


def finalTeacherSearch(message, headers, par):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text

        teacherData = getTeacherIdForUse(headers, par)
        teacherId = extractTeacherId(teacherData)
        print("Find by teacher: done")

        par = teacherId

        markup = botMarkup.mainMenuMarkup()
        schedule = getScheduleByTeacher(headers,par)
        formatedSchedule = scheduleCreator(schedule, None)
        if formatedSchedule == " ":
                formatedSchedule = "Розклад для цього викладача відсутній"
        tbot.send_message(chat_id=message.chat.id, text= formatedSchedule, reply_markup = markup)
    

def finalGroupSearch(message, headers, par):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text
        groupData = getGroupByNumber(headers, par)
        groupId = extractGroupId(groupData)
        print("Find by group: done")

        par = groupId

        markup = botMarkup.mainMenuMarkup()
        schedule = getScheduleByGroup(headers,par)
        formatedSchedule = scheduleCreator(schedule, None)
        if formatedSchedule == " ":
                formatedSchedule = "Розклад для цієї групи відсутній"
        tbot.send_message(chat_id=message.chat.id, text= formatedSchedule, reply_markup = markup)

def showGroups(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text

        groupsByCourse = groupByCourse(headers, par)
        groupsButtonNames = groupsList(groupsByCourse)
        print("Find by group: group")

        markup = botMarkup.fiveMarkup(groupsButtonNames)
        tbot.send_message(chat_id=message.chat.id, text= "Оберіть групу:", reply_markup=markup)
        tbot.register_next_step_handler(message, finalGroupSearch, headers, par)

def showTeachers(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text

        teachersByDiscipline = teacherByDiscipline(headers, par)
        teacherButtonNames = teachersList(teachersByDiscipline)
        print("Find by teacher: teacher")

        markup = botMarkup.tripleMarkup(teacherButtonNames)
        tbot.send_message(chat_id=message.chat.id, text= "Оберіть викладача:", reply_markup=markup)
        tbot.register_next_step_handler(message, finalTeacherSearch, headers, par)



#------------------------------------ Registration Block ------------------------------------------
def registerAsTeacher(headers,message):
    
    disciplines = disciplinesApi(headers)
    disciplinesButtonsNames = disciplinesList(disciplines)
    print("Register as teacher: discipline")

    userId = message.from_user.id
    markup = botMarkup.tripleRegMarkup(disciplinesButtonsNames, userId, headers)
    tbot.send_message(chat_id=message.chat.id, text= "Виберіть вашу дисципліну:", reply_markup=markup)



def registerAsStudent(headers,message):

    courses = coursesApi(headers)
    coursesButtonsNames = coursesList(courses)
    print("Register as student: course")
    
    userId = message.from_user.id
    markup = botMarkup.doubleRegMarkup(coursesButtonsNames, userId, headers)
    tbot.send_message(chat_id=message.chat.id, text= "Оберіть курс вашої групи:", reply_markup=markup)



def getTeachersNames(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text
        teachersByDiscipline = teacherByDiscipline(headers, par)
        teacherButtonNames = teachersList(teachersByDiscipline)
        print("Register as teacher: teacher")

        userId = message.from_user.id
        markup = botMarkup.tripleRegMarkup(teacherButtonNames, userId, headers)
        tbot.send_message(chat_id=message.chat.id, text= "Оберіть себе:", reply_markup=markup)

        tbot.register_next_step_handler(message, getRegTeacherId, headers)
    
    
def getGroupsNumbers(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text

        groupsByCourse = groupByCourse(headers, par)
        groupsButtonNames = groupsList(groupsByCourse)
        print("Register as group: group")

        userId = message.from_user.id
        markup = botMarkup.fiveRegMarkup(groupsButtonNames, userId, headers)
        tbot.send_message(chat_id=message.chat.id, text= "Оберіть групу:", reply_markup=markup)
        tbot.register_next_step_handler(message, getRegGroupId, headers)



def getRegTeacherId(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
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

        tbot.send_message(chat_id=message.chat.id, text = "Ви зареєструвалися, перевірити правильність можна у вкладці 'Допомога'", reply_markup=markup)


def getRegGroupId(message, headers):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text
        groupData = getGroupByNumber(headers, par)
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
                
        tbot.send_message(chat_id=message.chat.id, text = "Ви зареєструвалися,, перевірити правильність можна у вкладці 'Допомога'", reply_markup=markup)



def showCollegeFloor(message):
    if MainMenuCheck(message):
        returnToMainMenu(message)
    else:
        par = message.text
        markup = botMarkup.mainMenuMarkup()
        print("Show " + par + " floor")
       
        imageName = "data/" + par + ".jpg"
        tbot.send_photo(chat_id=message.chat.id, photo=open(imageName, 'rb'), reply_markup = markup)


#----------------------------Main Thread-------------------------------
def main():    

    tbot.infinity_polling()
    
if __name__ == "__main__":
    main()