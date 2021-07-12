from config import config
import telebot
from web import URLFunctions

bot = telebot.TeleBot(config.TOKEN_BOT)

#Сообщение об удачной подписке
def successful_sub_attempt_message(user_id, repos_url):
    bot.send_message(user_id, "Вы успешно подписались на репозиторий " + repos_url +" !",disable_web_page_preview=1)

#Сообщение об неудачной подписке
def unsuccessful_sub_attempt_message(user_id, repos_url):
    bot.send_message(user_id, "Вы уже подписаны на репозиторий " + repos_url  + " !",disable_web_page_preview=1)

#Сообщение об неудачной отписке
def unsuccessful_unsub_attemp_message(user_id, repos_url):
    bot.send_message(user_id, "Вы не были подписаны на репозиторий " + repos_url + " !",disable_web_page_preview=1)

#Сообщение об удачной отписке
def successful_unsub_attemp_message(user_id, repos_url):
    bot.send_message(user_id, "Вы отписались от репозитория " + repos_url + " !",disable_web_page_preview=1)

#Сообщение о неправильном имени репозитория
def wrong_repos_message(user_id, repos_url):
    bot.send_message(user_id, "Имя " + repos_url + " не может быть у репозитория !", disable_web_page_preview=1)

#Сообщение о том, что репозиторий не существует
def non_existing_repos(user_id, repos_url):
    bot.send_message(user_id, "Репозиторий " + repos_url + " не существует !", disable_web_page_preview=1)

#Сообщение с информацией о командах бота /info
def info_message(message):
    bot.send_message(message.chat.id, "<b>/info</b> - текстовое описание функционала бота\n"
                                      "<b>/subscribe</b> [repo_url]  - добавление репозитория в мои подписки\n"
                                      "  <u>Например</u>: /subscribe https://github.com/symfony/symfony\n"
                                      "<b>/unsubscribe</b> [repo_url]  - удаление репозитория из моих подписок\n"
                                      "  <u>Например</u>: /unsubscribe https://github.com/symfony/symfony\n"
                                      "<b>/list</b> - вывод списка репозиториев, на которые пользователь подписан\n"
                                      "<b>/news</b> - список обновлений по избранным репозиториям (коммиты в мастер) за последние сутки\n"
                                      "<b>/recommendations</b> - рекомендованные популярные репозитории\n",
                     parse_mode='html', disable_web_page_preview=1)

#Приветственное сообщение /start
def start_message(message):
    bot.send_message(message.chat.id, "Приветствую, {0.first_name}!\n"
                                      "Это бот для управления подписками Github.\n"
                                      "Чтобы увидеть список команд бота введите /info.".format(message.from_user)
                     )

#Сообщение, если команды не существует
def non_command_message(message):
    bot.send_message(message.chat.id, "У меня нет такой команды :)")

#Сообщение, если вызван /list или /news , но у пользователя нет подписок
def empty_list_command_message(user_id):
    bot.send_message(user_id, "У вас в подписках нет ни одного репозитория!")

#Сообщение, если есть подсписки и вызван /list
def not_empty_list_of_command_message(user_id,list):
    text_of_message = "Репозитории на которые вы подписаны:\n"
    for i in range(0,len(list),1):
        text_of_message += list[i].split('/')[3]+ '/' + list[i].split('/')[4] + " : " + list[i] + "\n"
    bot.send_message(user_id, text_of_message, disable_web_page_preview=1)

#Сообщение, если есть подсписки и вызван /news
def news_command_message(user_id, list):
    text = ''
    for i in range(0, len(list), 1):
        text += '<b>' + list[i].split('/')[3]+ '/' + list[i].split('/')[4] + '</b>' + " :\n" + URLFunctions.get_news(repos_url=list[i])
    bot.send_message(user_id, text, disable_web_page_preview=1,parse_mode='html')

#Сообщение, после вызова команды /recommendations
def rec_command_message(user_id, text):
    bot.send_message(user_id, text, disable_web_page_preview=1)

def api_error(user_id,text):
    bot.send_message(user_id, text , disable_web_page_preview=1)

