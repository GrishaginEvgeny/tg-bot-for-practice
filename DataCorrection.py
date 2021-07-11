from database import DBLogic

#Функция, которая преобразует list из библиотеки в py-список, лист состоит из подписок человека
def get_py_list(user_id):
    my_list_of_user = []
    for i in range(0,len(DBLogic.get_list(user_id=user_id)),1):
        my_list_of_user.append(DBLogic.get_list(user_id=user_id)[i][0])
    return my_list_of_user
