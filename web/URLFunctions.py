import random
import re
import datetime
import requests


#!!!---check-функции---!!!

#Проверка на гитхабоподобную ссылку
def check_url_for_valid(repos_url):
    flag = False
    if(repos_url.startswith('https://github.com')):
        flag = True
    elif(repos_url.startswith('github.com')):
        flag = True
    else:
        flag = False
    return flag

#Проверка на формат ссылки(есть ли https:// в начале)/используется только после check_url_for_valid
def check_valid_url_for_format(repos_url):
    flag = False
    if(repos_url.startswith('https://') == False):
        flag = False
    else:
        flag = True
    return flag

#Проверка на слеш в конце ссылки/используется только после check_url_for_valid
def check_slash_url(repos_url):
    if(repos_url.endswith('/')):
        return True
    else:
        return False

#Проверка ссылки по регулярному выражению/используется только после check_url_for_valid
def check_url_for_regex(repos_url):
    flag = False
    if(re.match(pattern="^/+([a-zA-Z][a-zA-Z0-9]*?([-][a-zA-Z0-9]+){0,2})+/[a-zA-Z0-9-]+[a-zA-Z0-9-]+/$",string=repos_url[18:])):
        flag = True
    else:
        flag = False
    return flag

#Проверка на существования самого репозитория(если все проверки на ввод пройдены)
def check_url_for_existing_repos(repos_url):
    headers = {
        'Content-type': 'application/json',
    }
    url = 'https://api.github.com/repos/' + repos_url.split('/')[3] + '/' + repos_url.split('/')[4]

    response = requests.get(url, headers=headers)
    try:
        a = response.json()['message']
        return False
    except KeyError:
        return True

#Проверка на то, кто владелец репозитория(группа - return True, пользователь - return False)
def check_for_repos_owner(repos_url):
    headers = {
        'Content-type': 'application/json',
    }

    url = 'https://api.github.com/repos/' + repos_url.split('/')[3] + '/' + repos_url.split('/')[4]

    response = requests.get(url, headers=headers)

    if(response.json()['owner']['type'] == 'User'):
        return False
    else:
        return True

#!!!---get-функции---!!!

#Функция, которая приводит ссылки к правильному формату
def get_valid_format_url(repos_url):
        return 'https://' + repos_url

#Функция, которая возвращает ссылку на страницу с коммитами

#Функция, которая возвращает правильную ссылку после всех проверок
def get_url(repos_url):
    if (check_valid_url_for_format(repos_url)):
        url = repos_url
        if (check_slash_url(url)):
            if (check_url_for_regex(url)):
                return url
            else:
                return ''
        else:
            url = url + '/'
            if (check_slash_url(url)):
                if (check_url_for_regex(url)):
                    return url
                else:
                    return ''
    else:
        url = get_valid_format_url(repos_url)
        if (check_slash_url(url)):
            if (check_url_for_regex(url)):
                return url
            else:
                return ''
        else:
            url = url + '/'
            if (check_slash_url(url)):
                if (check_url_for_regex(url)):
                    return url
                else:
                    return ''

#Функция, которая возвращает новости
def get_news(repos_url):
    headers = {
        'Content-type': 'application/json',
    }

    td = 0

    if (datetime.datetime.utcnow() > datetime.datetime.now()):
        td = (datetime.datetime.utcnow() - datetime.datetime.now()).seconds / 3600
        print(td)
    else:
        td = (datetime.datetime.now() - datetime.datetime.utcnow()).seconds / 3600
        print(td)
    print(datetime.datetime.now())

    text =""

    url = 'https://api.github.com/repos/' + repos_url.split('/')[3] + '/' + repos_url.split('/')[4] +'/commits'

    response = requests.get(url, headers=headers)

    for i in response.json():
        date = i['commit']['author']['date'][0:10].split('-')
        time = i['commit']['author']['date'][11:19].split(':')
        if ((datetime.datetime.now() - (datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])) + datetime.timedelta(hours=td))).days < 1):
            text += i['html_url'] +'\n'

    return text


def get_rec_from_group(repos_url):
    headers = {
        'Content-type': 'application/json',
    }

    a = []

    url = 'https://api.github.com/orgs/' + repos_url.split('/')[3] + '/repos'

    response = requests.get(url, headers=headers)

    for i in response.json():
        if repos_url.split('/')[3]+'/' +repos_url.split('/')[4] != i['full_name']:
            a.append(i['html_url'])

    return a[random.randint(0,len(a))]

def get_rec_from_users(repos_url):
    headers = {
        'Content-type': 'application/json',
    }

    a = []

    url = 'https://api.github.com/users/' + repos_url.split('/')[3] + '/repos'

    response = requests.get(url, headers=headers)

    for i in response.json():
        if repos_url.split('/')[4] != i['name']:
            a.append(i['html_url'])

    return a[random.randint(0, len(a))]