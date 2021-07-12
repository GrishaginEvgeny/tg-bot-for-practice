import random

from database import DBLogic
import Notifications
import DataCorrection
from web import URLFunctions

#Функция подписки, которая использует функции из БД
def subscribe(user_id, user_name, repos_url):
    if(URLFunctions.check_url_for_valid(repos_url) == True):
        url = URLFunctions.get_url(repos_url=repos_url)
        if(url != ''):
            if(URLFunctions.check_url_for_existing_repos(url) == True):
                if ((DBLogic.check_existing_user(user_id) == False) and (DBLogic.check_existing_repos(url) == False)):
                    DBLogic.user_add_to_db(user_name=user_name, id_chat_foo=user_id)
                    DBLogic.repos_add_to_db(url)
                    DBLogic.sub_add_to_db(user_id=user_id,rep_url=url)
                    Notifications.successful_sub_attempt_message(user_id=user_id, repos_url=url)
                elif((DBLogic.check_existing_user(user_id) == True) and (DBLogic.check_existing_repos(url) == False)):
                    DBLogic.repos_add_to_db(url)
                    DBLogic.sub_add_to_db(user_id=user_id,rep_url=url)
                    Notifications.successful_sub_attempt_message(user_id=user_id, repos_url=url)
                elif ((DBLogic.check_existing_user(user_id) == False) and (DBLogic.check_existing_repos(url) == True)):
                    DBLogic.user_add_to_db(user_name=user_name, id_chat_foo=user_id)
                    DBLogic.sub_add_to_db(user_id=user_id, rep_url=url)
                    Notifications.successful_sub_attempt_message(user_id, url)
                elif(((DBLogic.check_existing_user(user_id) == True) and (DBLogic.check_existing_repos(url) == True))):
                    if(DBLogic.check_existing_subs(id_u=user_id,id_r=DBLogic.find_repos(url)) == False):
                        DBLogic.sub_add_to_db(user_id=user_id, rep_url=url)
                        Notifications.successful_sub_attempt_message(user_id=user_id, repos_url=url)
                    else:
                        Notifications.unsuccessful_sub_attempt_message(user_id=user_id, repos_url=url)
            else:
                Notifications.non_existing_repos(user_id=user_id,repos_url=url)
        else:
            Notifications.wrong_repos_message(user_id=user_id, repos_url=repos_url)
    else:
        Notifications.wrong_repos_message(user_id=user_id,repos_url=repos_url)

#Функция отписки, которая использует функции из БД
def unsubscribe(user_id, repos_url):
    if (URLFunctions.check_url_for_valid(repos_url) == True):
        url = URLFunctions.get_url(repos_url=repos_url)
        if(url != ''):
            if (URLFunctions.check_url_for_existing_repos(url) == True):
                if (DBLogic.check_existing_subs(id_u=user_id, id_r=DBLogic.find_repos(url)) == False):
                    Notifications.unsuccessful_unsub_attemp_message(user_id=user_id, repos_url=url)
                else:
                    DBLogic.delete_subs(id_user=user_id, id_repos=DBLogic.find_repos(url))
                    Notifications.successful_unsub_attemp_message(user_id=user_id, repos_url=url)
            else:
                Notifications.non_existing_repos(user_id=user_id,repos_url=url)
        else:
            Notifications.wrong_repos_message(user_id=user_id, repos_url=repos_url)
    else:
        Notifications.wrong_repos_message(user_id=user_id, repos_url=repos_url)

#Функция вывода всех подписок, которая использует функции из БД
def list(user_id):
    if(len(DataCorrection.get_py_list(user_id=user_id)) == 0):
        Notifications.empty_list_command_message(user_id=user_id)
    else:
        Notifications.not_empty_list_of_command_message(user_id=user_id,list=DataCorrection.get_py_list(user_id=user_id))

#Функция вывода всех новинок, которая использует функции из БД
def news(user_id):
    list = DataCorrection.get_py_list(user_id=user_id)
    if (len(list) == 0):
        Notifications.empty_list_command_message(user_id=user_id)
    else:
        Notifications.news_command_message(user_id=user_id, list=list)

def recommendations(user_id):
    list = DataCorrection.get_py_list(user_id=user_id)
    text = 'Ваши рекомендации:\n'
    if(len(list) == 0):
        Notifications.empty_list_command_message(user_id=user_id)
    else:
        flag = False
        if (len(list) < 3):
            for l in list:
                if(URLFunctions.check_for_repos_owner(repos_url=l) == 3):
                    Notifications.api_error(user_id=user_id, text='Проблемы с подключением к репозиторию ' + list[l])
                    flag = True
                elif (URLFunctions.check_for_repos_owner(repos_url=l) == 2):
                    text += URLFunctions.get_rec(repos_url=l, flag=True, list=list) + '\n'
                elif (URLFunctions.check_for_repos_owner(repos_url=l) == 1):
                    text += URLFunctions.get_rec(repos_url=l, flag=False, list=list) + '\n'
        else:
            a = []
            while len(a) != 3:
                 b = random.randint(0,len(list)-1)
                 if b not in a:
                     a.append(b)
            for i in range(0, 3, 1):
                if(URLFunctions.check_for_repos_owner(repos_url=list[a[i]]) == 3):
                    Notifications.api_error(user_id=user_id, text='Проблемы с подключением к репозиторию ' + list[a[i]])
                    flag = True
                elif(URLFunctions.check_for_repos_owner(repos_url=list[a[i]]) == 2):
                    text += URLFunctions.get_rec(repos_url=list[a[i]],flag=True,list=list) + '\n'
                elif(URLFunctions.check_for_repos_owner(repos_url=list[a[i]]) == 1):
                    text += URLFunctions.get_rec(repos_url=list[a[i]],flag=False,list=list) + '\n'
        if(flag != True):
            Notifications.rec_command_message(user_id=user_id, text=text)
