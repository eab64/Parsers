from bs4 import BeautifulSoup
import requests
import pymysql
import pymysql.cursors
import datetime

def str_to_datetime(string):#преобразователь даты к типу datetime
    if ("Января" in string):
        string = string.replace("Января", "January")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Февраля" in string):
        string = string.replace("Февраля", "February")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Марта" in string):
        string = string.replace("Марта", "March")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Апреля" in string):
        string = string.replace("Апреля", "April")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Мая" in string):
        string = string.replace("Мая", "May")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Июня" in string):
        string = string.replace("Июня", "June")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Июля" in string):
        string = string.replace("Июля", "July")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Августа" in string):
        string = string.replace("Августа", "August")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Сентября" in string):
        string = string.replace("Сентября", "September")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Октября" in string):
        string = string.replace("Октября", "October")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Ноября" in string):
        string = string.replace("Ноября", "November")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("Декабря" in string):
        string = string.replace("Декабря", "December")
        date_time = datetime.datetime.strptime(string, '%d %B %Y, %H:%M')
        return date_time
    if ("сегодня" in string):
        string = string.replace("сегодня",
                                str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(
                                    datetime.datetime.now().year))
        date_time = datetime.datetime.strptime(string, '%d/%m/%Y, %H:%M')
        return date_time
    if ("вчера" in string):
        string = string.replace("вчера", str(datetime.datetime.now().day - 1) + "/" + str(
            datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year))
        date_time = datetime.datetime.strptime(string, '%d/%m/%Y, %H:%M')
        return date_time

url = 'https://tengrinews.kz/kazakhstan_news/glava-minzdrava-prokommentiroval-video-aynyi-bakeevoy-407335/'
base_url = 'https://tengrinews.kz'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')
news = soup.find_all('div', class_='tn-tape-item')#получаем все ссылки новостей
links = []
for item in news:
    links.append(base_url + item.find('a',class_='tn-tape-title').get('href'))#закидываем в список все ссылки

args = []
for url in links:#пробегаемся по всем ссылкам и ищем инфу
    response = requests.get(url)#делаем запрос
    html = response.text#получаем html
    soup = BeautifulSoup(html, 'html.parser')#делаем из html soup
    title = soup.select_one('h1').text#находим все названия
    data = soup.find('div', class_='tn-side-bar').find('time').text#находим все даты
    time = soup.find('div', class_='tn-side-bar').find('time').text#находим тайминги
    content = soup.find('div', class_='tn-news-text').text#находим весь контент
    args.append((url,title,content,str_to_datetime(data),time))#закидываем все 5 в 1 список


connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = 'root',
                             db = 'new_data',
                             charset = 'utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)#соединение с базой данных
print("connect successful")

try:
    for ar in args:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `my_table` (`link`, `title`, `content`,`publish_date`,`date_time`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, ar)#в цикле закидываем весь список по элементу
        connection.commit()
finally:
    connection.close()