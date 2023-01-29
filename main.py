from time import sleep
from tokenize import group
from telebot import TeleBot
from buttons import *
from courses import coursesList
from groups import groupsList
from disciplines import disciplinesList
from common.Constants import Constants
from groups import groupsList
import markup as botMarkup
from apiService import *
from register import *
from teachers import *
from users import getUserId

tag: str = "BOT"
headers = authenticate()
tbot = TeleBot(Constants.botToken)

coursesButtonsNames = coursesButtonsNames = coursesList(coursesApi(headers))
groupsButtonNames = []
teacherButtonNames = []
disciplinesButtonsNames = disciplinesButtonsNames = disciplinesList(disciplinesApi(headers))
paramater = ""
logger = False

#тут був стакан

@tbot.message_handler(commands=["start"])
def start(message):

    global logger

    logger = False
    userId = message.from_user.id
    if checkUser(userId, headers):
        markup = botMarkup.mainMenuMarkup()
        print("/start: user already exists")
        tbot.send_message(chat_id=message.chat.id, text = "Ми вас вже знаємо!", reply_markup=markup)
        logger = True
    else: 
        replyMessage = "Зареєструйтеся. Оберіть хто ви:"
        print("/start: user registration")
        markup = botMarkup.registerMarkup()
        tbot.send_message(chat_id=message.chat.id, text=replyMessage, reply_markup=markup)


@tbot.message_handler(commands=["change"])
def start(message):

    global logger

    logger = False
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
    global parameter

    global logger

    if logger == False:
        if message.text ==  Register.TEACHER.value:
            registerAsTeacher(headers, message)

        if message.text ==  Register.STUDENT.value:
            registerAsStudent(headers, message)

        if message.text in coursesButtonsNames:
            parameter = groupGetNames(message, headers) 
            groupsButtonNames = groupsList(groupByCourse(headers, parameter))

        if message.text in disciplinesButtonsNames:
            parameter = teacherGetNames(message, headers)
            teacherButtonNames = teachersList(teacherByDiscipline(headers, parameter))    

        if message.text in groupsButtonNames:
            userId = message.from_user.id
            groupRegId = groupRegID(message, headers, parameter)
            logger = True

            userData = {
	        "id": "{}".format(userId),
	        "groupId":"{}".format(groupRegId)
            }

            register(userData, headers, userId)
            markup = botMarkup.mainMenuMarkup()
            userData = getUserId(getUserById(userId, headers))
            
            tbot.send_message(chat_id=message.chat.id, text = "Ви зареєструвалися, індекс групи {}".format(userData.id), reply_markup=markup)

        if message.text in teacherButtonNames:
            userId = message.from_user.id
            teacherRegId = teacherRegID(message, headers, parameter)
            logger = True

            userData = {
	        "id": "{}".format(userId),
	        "teacherId":"{}".format(teacherRegId)
            }

            register(userData, headers, userId)
            markup = botMarkup.mainMenuMarkup()
            userData = getUserId(getUserById(userId, headers))

            tbot.send_message(chat_id=message.chat.id, text = "Ви зареєструвалися, індекс викладача {}".format(userData.id), reply_markup=markup)


    if logger == True:
        if message.text ==  MainMenuButtons.FIND_BY_TEACHER.value:
            userId= message.from_user.id

            disciplines = disciplinesApi(headers)
            disciplinesButtonsNames = disciplinesList(disciplines)
            print("Find by teacher: discipline")
            
            markup = botMarkup.tripleMarkup(disciplinesButtonsNames)
            tbot.send_message(chat_id=message.chat.id, text= "Виберіть дисципліну викладача:", reply_markup=markup)

            return

        
        if message.text ==  MainMenuButtons.FIND_BY_GROUP.value:
            userId = message.from_user.id

            courses = coursesApi(headers)
            coursesButtonsNames = coursesList(courses)
            print("Find by group: course")
            
            markup = botMarkup.doubleMarkup(coursesButtonsNames)
            tbot.send_message(chat_id=message.chat.id, text= "Оберіть курс групи:", reply_markup=markup)

            return

        if message.text == MainMenuButtons.FIND_BY_DAY.value:
            markup = botMarkup.findByDayWMarkup()
            print("Find by day")
            tbot.send_message(chat_id=message.chat.id, text="Повертаємося у головне меню", reply_markup=markup)

            return

        if message.text == MainMenuButtons.MAIN_MENU.value:
            markup = botMarkup.mainMenuMarkup()
            print("Main menu")
            tbot.send_message(chat_id=message.chat.id, text="Повертаємося у головне меню", reply_markup=markup)

            return
        
        if message.text in coursesButtonsNames:
            par = message.text

            groupsByCourse = groupByCourse(headers, par)
            groupsButtonNames = groupsList(groupsByCourse)
            print("Find by group: group")

            markup = botMarkup.fiveMarkup(groupsButtonNames)
            tbot.send_message(chat_id=message.chat.id, text= "Оберіть групу:", reply_markup=markup)

            return

        if message.text in disciplinesButtonsNames:
            par = message.text

            teachersByDiscipline = teacherByDiscipline(headers, par)
            teachersButtonNames = teachersList(teachersByDiscipline)
            print("Find by teacher: teacher")

            markup = botMarkup.tripleMarkup(teachersButtonNames)
            tbot.send_message(chat_id=message.chat.id, text= "Оберіть викладача:", reply_markup=markup)

            return
        
        #userData.id = id of teacher or group, userData.isStudent = true or false
        #userData = getUserId(getUserById(userId, headers))


def main():
    

    tbot.infinity_polling()
    
if __name__ == "__main__":
    main()