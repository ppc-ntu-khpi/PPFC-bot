from telebot import types

from buttons import *
from utils import chunks


def mainMenuMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)

    button1 = types.KeyboardButton(MainMenuButtons.SCHEDULE_TODAY.value)
    button2 = types.KeyboardButton(MainMenuButtons.SCHEDULE_TOMORROW.value)

    button3 = types.KeyboardButton(MainMenuButtons.CHANGES_TODAY.value)
    button4 = types.KeyboardButton(MainMenuButtons.CHANGES_TOMORROW.value)

    button5 = types.KeyboardButton(MainMenuButtons.FIND_BY_TEACHER.value)
    button6 = types.KeyboardButton(MainMenuButtons.FIND_BY_GROUP.value)
    button7 = types.KeyboardButton(MainMenuButtons.FIND_BY_DAY.value)

    button8 = types.KeyboardButton(MainMenuButtons.ADDITIONAL_FUNCTIONS.value)
    button9 = types.KeyboardButton(MainMenuButtons.HELP.value)

    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5, button6, button7)
    markup.row(button8, button9)

    return markup

def findByDayWMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)

    button1 = types.KeyboardButton(FindByDayButtons.MONDAY.value)
    button2 = types.KeyboardButton(FindByDayButtons.TUESDAY.value)
    button3 = types.KeyboardButton(FindByDayButtons.WEDNESDAY.value)

    button4 = types.KeyboardButton(FindByDayButtons.THURSDAY.value)
    button5 = types.KeyboardButton(FindByDayButtons.FRIDAY.value)

    mainMenu = types.KeyboardButton(MainMenuButtons.MAIN_MENU.value)

    markup.row(button1, button2,button3)
    markup.row(button4, button5)
    markup.row(mainMenu)


    return markup

def registerMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)

    button1 = types.KeyboardButton(Register.STUDENT.value)
    button2 = types.KeyboardButton(Register.TEACHER.value)

    markup.row(button1, button2)

    return markup


def fiveMarkup(Names):
    rows = chunks(Names, 5)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    for row in rows:
        buttonsRow = []
        
        for button in row:
            buttonsRow.append(types.KeyboardButton(button))

        markup.row(*buttonsRow)
    buttonMain = types.KeyboardButton(MainMenuButtons.MAIN_MENU.value)
    markup.row(buttonMain)
    return markup

def doubleMarkup(Names):
    rows = chunks(Names, 2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    for row in rows:
        buttonsRow = []
        
        for button in row:
            buttonsRow.append(types.KeyboardButton(button))

        markup.row(*buttonsRow)
    buttonMain = types.KeyboardButton(MainMenuButtons.MAIN_MENU.value)
    markup.row(buttonMain)
    return markup

def tripleMarkup(Names):
    rows = chunks(Names, 3)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    for row in rows:
        buttonsRow = []
        
        for button in row:
            buttonsRow.append(types.KeyboardButton(button))

        markup.row(*buttonsRow)
    buttonMain = types.KeyboardButton(MainMenuButtons.MAIN_MENU.value)
    markup.row(buttonMain)
    return markup

def tripleRegMarkup(Names):
    rows = chunks(Names, 3)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    for row in rows:
        buttonsRow = []
        
        for button in row:
            buttonsRow.append(types.KeyboardButton(button))

        markup.row(*buttonsRow)
    return markup

def doubleRegMarkup(Names):
    rows = chunks(Names, 2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    for row in rows:
        buttonsRow = []
        
        for button in row:
            buttonsRow.append(types.KeyboardButton(button))

        markup.row(*buttonsRow)
    return markup

def fiveRegMarkup(Names):
    rows = chunks(Names, 5)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    for row in rows:
        buttonsRow = []
        
        for button in row:
            buttonsRow.append(types.KeyboardButton(button))

        markup.row(*buttonsRow)
    return markup

def additionalFuncMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)

    button1 = types.KeyboardButton(AdditionalFuncButtons.RINGS_SCHEDULE.value)
    button2 = types.KeyboardButton(AdditionalFuncButtons.EDU_PROCESS.value)

    button3 = types.KeyboardButton(AdditionalFuncButtons.COLLEGE_MAP.value)
    button4 = types.KeyboardButton(AdditionalFuncButtons.WORK_SATURDAYS.value)

    button5 = types.KeyboardButton(AdditionalFuncButtons.CHANGE_DATA.value)
    mainMenu = types.KeyboardButton(MainMenuButtons.MAIN_MENU.value)

    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    markup.row(mainMenu)

    return markup

def collegeMapMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = False)
    button1 = types.KeyboardButton(CollegeFloors.FIRST_FLOOR.value)
    button2 = types.KeyboardButton(CollegeFloors.SECOND_FLOOR.value)

    button3 = types.KeyboardButton(CollegeFloors.THIRD_FLOOR.value)
    mainMenu = types.KeyboardButton(MainMenuButtons.MAIN_MENU.value)

    markup.row(button1, button2, button3)
    markup.row(mainMenu)

    return markup