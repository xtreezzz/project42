from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
import logging
from datetime import datetime
import telegram
import os
import csv
import sys
from code_py.model import Gamer, db_session
from sqlalchemy import exists, and_
import re

sys.path.append(os.path.abspath(__file__))
log_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir_path, exist_ok=True)
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename=f"logs/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

                    )
logging.getLogger().addHandler(logging.StreamHandler())

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    chat_id = update.message.chat_id
    # msg_date = update.message.date
    user = update.message.from_user
    user_exist_flag = db_session.query(exists().where(and_(Gamer.first_name == user.first_name, Gamer.last_name == user.last_name,
                                               Gamer.chat_id == chat_id))).scalar()
    if user_exist_flag:
        flag = 'Старичок'
    else:
        user = Gamer(first_name=user.first_name, last_name=user.last_name, chat_id=chat_id, nick_name=user.username)
        db_session.add(user)
        db_session.commit()
        flag = 'Новичок'



    update.message.reply_text(f"{flag}, {user.last_name} {user.first_name} <3", reply_markup=user_keyboard())


def send_quiz_message(bot, update):
    # TODO отказаться от хардкода и забирать текущий список из базы
    global today_command_list
    today_command_list = [153799581, 510364397]
    user_text = update.message.text
    input_list = update.message.text.split('send')[1].strip()
    print(input_list, today_command_list)

    for id in today_command_list:
        bot.sendMessage(chat_id=id, text="Stay here, I'll be back.")

#TODO создать keyboard.py
def user_keyboard():
    # двойной ряд только
    _user_keyboard = ReplyKeyboardMarkup([
        ['*Зарегистрироваться🙈', '*Отредактировать анкету']
        , ['*Посмотреть состав команды', '*Посмотреть статистику']
        , ['Капитанский мостик']
        , ['*Пойти на игру']
        , ['*Задать вопрос организаторам', '*Задать вопрос', 'Активное голосование', 'Оставить отзыв']
        , ['*Check in', '*Конкурс инстаграмм', 'Голосование']
    ], resize_keyboard=True)
    print('olol')
    return _user_keyboard


def team_keyboard():
    _team_keyboard = ReplyKeyboardMarkup([
        ['Создать команду', '*Отредактировать анкету', '*Отредактировать состав']
        , ['*Зарегистрироваться на игру', '*Сменить капитана', '*Бросить вызов']
        , ['*Посмотреть статистику']
    ], resize_keyboard=True)
    return _team_keyboard


def game_team_keyboard():
    _game_team_keyboard = ReplyKeyboardMarkup([
        ['*Check in команду', '*Check in человека', '*Сменить капитана']
        , ['*Посмотреть все команды']
        , ['*Посмотреть результаты']

    ], resize_keyboard=True)
    return _game_team_keyboard


def game_stat():
    # Посмотреть результат команды
    # Посмотреть свой команды
    pass


def chat_listener(bot, update):
    user_text = update.message.text
    user = update.message.from_user

    # if user.id == ADMIN_ID:
    #     update.message.reply_text('Welcome Master')
    # else:
    #     update.message.reply_text(f'Welcome HALOP your text{user_text}')

#TODO создать flow.py
def team_reg(bot, update, user_data):
    update.message.reply_text("Введите название вашей команды", reply_markup=ReplyKeyboardRemove())
    return "name"


def team_menu_func(bot, update, user_data):
    update.message.reply_text(f"Командное меню", reply_markup=team_keyboard())


def team_get_name(bot, update, user_data):
    team_name = update.message.text
    if team_name == 'Ris':
        update.message.reply_text('Кис по братски')
        return "name"
    else:
        user_data['team_name'] = team_name
        update.message.reply_text("""Пожалуйста введите слоган вашей команды 
или /skip""")
        return "slogan"


def team_slogan(bot, update, user_data):
    user_data['slogan'] = update.message.text
    update.message.reply_text("Введите номер телефона")
    return 'phone'


def team_slogan_skip(bot, update, user_data):
    user_data['slogan'] = ''
    update.message.reply_text("Введите номер телефона")
    return 'phone'


def team_slogan_sticker(bot, update, user_data):
    user_data['slogan'] = update.message.sticker.file_id
    update.message.reply_text("Введите номер телефона")
    return 'phone'


def team_get_phone(bot, update, user_data):
    phone = update.message.text
    #TODO найти нормальный regexp
    if re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone):
        user_data['team_phone'] = phone
        update.message.reply_text("""Пожалуйста введите email 
или /skip""")
        return "email"
    else:
        update.message.reply_text(f"Введите корректный номер телефона, а не {phone}")
        return 'phone'


def team_get_email(bot, update, user_data):
    email = update.message.text
    if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
        user_data['email'] = email
        update.message.reply_text(f"Вы зареганы {user_data}", reply_markup=user_keyboard())
        return ConversationHandler.END
    else:
        update.message.reply_text(f"Введите корректный email, а не {email}")
        return 'email'


def team_get_email_skip(bot, update, user_data):
    user_data['email'] = update.message.text
    update.message.reply_text(f"Вы зареганы {user_data}", reply_markup=user_keyboard())
    return ConversationHandler.END


def dontknow(bot, update, user_data):
    bot.send_sticker(chat_id=update.message.chat_id, sticker='CAADAgADIgADCA1lDqlm6Zo7g-xqAg')


def main():
    #TODO убрать токен в конфиг
    mybot = Updater('ХХХХХХ', request_kwargs=PROXY)
    # фильтры обрабатываются в порядке очереди
    dp = mybot.dispatcher
    team_menu = ConversationHandler(
        entry_points=[RegexHandler('^(Капитанский мостик)$', team_menu_func, pass_user_data=True)],
        states={},
        fallbacks=[]
    )
    team_menu_reg = ConversationHandler(
        entry_points=[RegexHandler('^(Создать команду)$', team_reg, pass_user_data=True)],
        states={
            "name": [MessageHandler(Filters.text, team_get_name, pass_user_data=True)],
            "slogan": [MessageHandler(Filters.text, team_slogan, pass_user_data=True),
                       MessageHandler(Filters.sticker, team_slogan_sticker, pass_user_data=True),
                       CommandHandler('skip', team_slogan_skip, pass_user_data=True)],
            "phone": [MessageHandler(Filters.text, team_get_phone, pass_user_data=True)],
            "email": [MessageHandler(Filters.text, team_get_email, pass_user_data=True),
                      CommandHandler('skip', team_get_email_skip, pass_user_data=True)]

        },
        #TODO заставить работать
        fallbacks=[MessageHandler(Filters.sticker, dontknow, pass_user_data=True)]
    )
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(team_menu)
    dp.add_handler(team_menu_reg)
    dp.add_handler(CommandHandler("send", send_quiz_message))
    dp.add_handler(MessageHandler(Filters.text, chat_listener))
    mybot.start_polling()
    mybot.idle()


main()
