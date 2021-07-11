from config import config
import telebot
from database import DB_Functions
import Notifications
import time

bot = telebot.TeleBot(config.TOKEN_BOT)

#!!!--- Команды ---!!!
#Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    Notifications.start_message(message)

#Команда /info
@bot.message_handler(commands=['info'])
def info_command_function(message):
    Notifications.info_message(message)

#Команда /subscribe
@bot.message_handler(commands=['subscribe'])
def subscribe_attempt(message):
   DB_Functions.subscribe(user_id=message.chat.id,user_name=message.from_user.first_name,repos_url= message.text[11:])

#команда /unsubscribe
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe_attempt(message):
    DB_Functions.unsubscribe(user_id=message.chat.id, repos_url=message.text[13:])

#команда /list
@bot.message_handler(commands=['list'])
def list_call_attempt(message):
    DB_Functions.list(message.chat.id)

#команда /news
@bot.message_handler(commands=['news'])
def news_call_attempt(message):
    DB_Functions.news(user_id=message.chat.id)

@bot.message_handler(commands=['recommendations'])
def recommendations_call_attempt(message):
    DB_Functions.recommendations(user_id=message.chat.id)

#при вводе неизвестных команд или любого другого текста
@bot.message_handler(content_types=['text'])
def non_command_reaction(message):
    Notifications.non_command_message(message)

#Запуск бота. Если он падает, то попытается сам запуститься через 15 минут.
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
