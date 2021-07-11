from database import DBLogic
import Notifications
import DataCorrection
from web import URLFunctions

#Функция подписки, которая использует функции из БД
def subscribe(user_id, user_name, repos_url):
    if(URLFunctions.check_url_for_valid(repos_url) == True):
        url = URLFunctions.get_url(repos_url=repos_url)
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
        Notifications.wrong_repos_message(user_id=user_id,repos_url=repos_url)

#Функция отписки, которая использует функции из БД
def unsubscribe(user_id, repos_url):
    if (URLFunctions.check_url_for_valid(repos_url) == True):
        url = URLFunctions.get_url(repos_url=repos_url)
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
        if (len(list) < 3):
            for l in list:
                if (URLFunctions.check_for_repos_owner(l)):
                    text += URLFunctions.get_rec_from_group(repos_url=l, id_user= user_id,list=list) + '\n'
                else:
                    text += URLFunctions.get_rec_from_users(repos_url=l, user_id=user_id,list=list) + '\n'
        else:
            for i in range(0, 3, 1):
                if (URLFunctions.check_for_repos_owner(list[i])):
                    text += URLFunctions.get_rec_from_group(repos_url=list[i],id_user= user_id,list=list) + '\n'
                else:
                    text += URLFunctions.get_rec_from_users(repos_url=list[i],user_id=user_id,list=list) + '\n'
        Notifications.rec_command_message(user_id=user_id, text=text)
