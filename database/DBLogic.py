import psycopg2
from config import config

#!!!---Добавление данных в БД ---!!!

#Функция, которая добавляет пользователя в БД
def user_add_to_db(user_name,id_chat_foo):
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO users (id_chat, name) VALUES (%s,%s);',(id_chat_foo,user_name))

#Функция, которая добавляет репозиторий в БД
def repos_add_to_db(url_of_rep):
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO repositories (url) VALUES (%s);',(url_of_rep, ))

#Функция, которая добавляет подписку в БД
def sub_add_to_db(user_id,rep_url):
        repos_id = find_repos(rep_url)
        with psycopg2.connect(config.DB_DSN) as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO subscribes (id_user, id_repos) VALUES (%s,%s);',(user_id,repos_id))

#!!!--- Проверка на повторение данных ---!!!

#Функция, которая проверяет существование пользователя в БД
def check_existing_user(user_id):
    flag = False
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id_chat FROM users WHERE id_chat = %s', (user_id, ))
            if(len(cursor.fetchall())!=0):
                flag = True
    return flag

#Функция, которая проверяет существование репозитория в БД
def check_existing_repos(rep_url):
    flag = False
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT url FROM repositories WHERE url = %s', (rep_url, ))
            if(len(cursor.fetchall())!=0):
                flag = True
    return flag

#Функция, которая проверяет существования подписки В БД
def check_existing_subs(id_r,id_u):
    flag = False
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id_repos,id_user FROM subscribes WHERE id_repos = %s and id_user = %s', (int(id_r),int(id_u)))
            if (len(cursor.fetchall()) != 0):
                flag = True
    return flag

#!!!--- Поиск данных в БД ---!!!

#Функция, которая возвращает id репозитория из БД
def find_repos(rep_url):
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id_repos FROM repositories WHERE url = %s', (rep_url, ))
            return cursor.fetchone()[0]

#Функция, которая выводит все подписки пользователя
def get_list(user_id):
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT url from subscribes inner join repositories r on r.id_repos = subscribes.id_repos inner join users u on u.id_chat = subscribes.id_user where id_chat=%s', (user_id,))
            return cursor.fetchall()


#!!!--- Удаление данных из БД ---!!!

#Функция, которая удаляет подписку на репозиторий из БД
def delete_subs(id_user, id_repos):
    with psycopg2.connect(config.DB_DSN) as conn:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM subscribes WHERE id_user = %s and id_repos = %s', (id_user,id_repos))


