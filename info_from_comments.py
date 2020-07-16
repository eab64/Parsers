from selenium import webdriver
import pymysql.cursors
import datetime
import requests
from bs4 import BeautifulSoup


def str_to_datetime_comments(string):
        date_time = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M')
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
#links = ['https://tengrinews.kz/world_news/stalo-izvestno-reaktsii-putina-prevraschenie-sobora-ayya-408417/']


comments =[]
for url in links:
    browser = webdriver.Firefox()#указали браузер
    browser.get(url)#открытие страницы
    element = browser.find_element_by_class_name('tn-icon-comment-dark')#поиск элемента для нажатия
    element.click()#нажимаем и раскрываем комментарий
    sum_com = browser.find_element_by_xpath('/html/body/div[2]/main/section/div/div[4]/div[1]/ul/li[1]/span').text#смотрим количество комментов
    if sum_com !="0":#если кол. комментов 0, дальше не ищем
        author = browser.find_element_by_class_name('tn-user-name').text#находим автора
        content = browser.find_element_by_class_name('tn-comment-item-content-text').text#находим текст
        try:
            date = browser.find_element_by_xpath("/html/body/div[2]/main/section/div/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/time").text#находим дату
            comments.append((url, author,content,str_to_datetime_comments(date)))#закидываем все данные в один список
            print(comments)
        except Exception:
            pass
        finally:
            browser.quit()




connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = 'root',
                             db = 'tengrinews',
                             charset = 'utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)#соединение с базой данных
print("connect successful")

try:
    for comment in comments:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `comments` (`link`, `author`, `comment`, `date_time`) VALUES (%s, %s, %s, %s)"#загрузка в базу данных
            cursor.execute(sql, comment)
    connection.commit()
finally:
    connection.close()