#coding: utf8
import feedparser
import unicodedata
from datetime import datetime
import cgi
import time
from bs4 import BeautifulSoup
import requests


print("Content-type: text/html; charset=utf-8")
print()
print("""<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="../css/main.css" type="text/css" charset="utf-8"></link>
    <title>Новости</title>
</head>
<body>
<section class="grid">
""")
#Сайт для парсинга с базой данных rss новостных сайтов
SUBSCRIBE_URL="https://subscribe.ru/catalog/media?rss"
HEADERS={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.111 YaBrowser/21.2.1.107 Yowser/2.5 Safari/537.36',
         'accept': '*/*'}

# rss_urls=[
#         {  'rss_link': 'https://meduza.io/rss2/all',
#            'rss_name': 'Медуза',
#            'site_link': 'https://meduza.io/'},
#             {'rss_link': 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss',
#            'rss_name': 'РБК Новости',
#             'site_link': 'https://www.rbc.ru/'},
#             {'rss_link': 'https://ria.ru/export/rss2/archive/index.xml',
#            'rss_name': 'РИА Новости',
#              'site_link': 'https://ria.ru/'},
#         {'rss_link': 'http://news.rambler.ru/rss/world/',
#            'rss_name': 'Рамблер Новости',
#          'site_link': 'https://news.rambler.ru/'},
#         {'rss_link': 'https://lenta.ru/rss',
#            'rss_name': 'Lenta.ru',
#          'site_link': 'https://lenta.ru/'},
#         {'rss_link': 'http://www.itar-tass.com/rss/all.xml',
#            'rss_name': 'ТАСС',
#          'site_link': 'https://tass.ru'},
#           ]

news = []

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#Парсим rss данные с сайта подписок
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='entry fullentry rss')
    rss_info=[]
    for item in items:
        rss_name_h = item.find( 'h2' )
        rss_name_a = rss_name_h.find( 'a' ).string
        rss_name = [line.rstrip('\n') for line in rss_name_a]

        rss_span = item.find( 'span' )
        rss_span_a = rss_span.find_all('a')
        #rss_link = rss_link_a.get('href')

        if len(rss_span_a)==2:
            rss_link = rss_span_a[0].string
        else: rss_link = ""
        if len(rss_span_a)==2:
            rss_rss = rss_span_a[1].string
        else: rss_rss = ""

        rss_info.append({
            'sub_name': "".join(rss_name),                                                                              #Название новостного сайта
            'sub_link': rss_link,                                                                                       #Адрес новостного сайта
            'sub_rss': rss_rss                                                                                          #RSS новостного сайта
        })
    return rss_info

#Запрос к subscribe.ru
def parse():
    html = get_html(SUBSCRIBE_URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        return print('error')

subscribe_info = parse()

count = 0
site_count = 20
for index, url in enumerate(subscribe_info):
    if url.get('sub_rss') != "":
        parser = feedparser.parse(url.get('sub_rss'))

    if index == site_count:                                                                                             #Заглушка. Указанное кол-во новостных сайтов с которых мы парсим
        break


    for entry in parser.entries:

        img_href = ""
        desc = ""

        if "description" in entry:                                                                                      #Проверка на основные RSS ключи. У некоторых сайтов эти отсутствуют
            if "published" in entry:
                desc = unicodedata.normalize("NFKD", entry.description)
                if "<div style=" and "<p>" in desc:                                                                     #Проверка на html код в описании. Такое есть в старых версиях RSS расслки
                    desc = ""
                else:
                    if desc != "":                                                                                      #Проверка на содержание описания новости, у некоторых сайтов она присутствует как поле, но пустая
                        new_published = unicodedata.normalize("NFKD", entry.published)
                        if "GMT" in new_published:
                            new_published.replace("GMT", "")
                            if new_published[0].isalpha():
                                published_time = datetime.strptime(new_published,
                                                                   '%a, %d %b %Y %X')
                            else:
                                published_time = datetime.strptime(new_published, '%d %b %Y %X')
                        else:
                            if new_published[0].isalpha():
                                published_time = datetime.strptime(new_published, '%a, %d %b %Y %X %z')                 # Проверка на разные форматы даты
                            else:
                                published_time = datetime.strptime(new_published, '%d %b %Y %X %z')


                        if entry.enclosures:
                            img_href = (entry.enclosures[0].get('href'))
                        news.append({                                                                                   #Конструктор новостной карточки
                            'title': unicodedata.normalize("NFKD", entry.title),                                        #Название
                            'description': desc,                                                                        #Описание
                            'origin_author': url.get('sub_name'),                                                       #Сайт автор
                            'link': unicodedata.normalize("NFKD", entry.link),                                          #Ссылка на новость
                            'link_site': url.get('sub_link'     ),                                                      #Ссылка на сам сайт
                            'published': str(published_time.strftime('%Y-%m-%d %H:%M')),                                #Дата публикации
                            'img_href': img_href                                                                        #Картинка
                        })
                        news.sort(key=lambda dictionary: dictionary['published'], reverse=True)

x = 0

for new in news:
    if new.get('img_href').endswith('.jpg'):                                                                            #Заглушка для картинки
        image_url = new.get('img_href')
    else:
        image_url = "../images/novosti.jpg"
    published_time = datetime.strptime(new.get('published'), '%Y-%m-%d %H:%M')

    desc = new.get('description')
    x = x + 1
    print('<article class="grid-item">'                                                                                 #Рендер  карточки
            '<div class="image">'
                '<img src='+ image_url,' />'
            '</div>'
            '<div class="info">'
                '<h2>' + new.get('title'), '</h2>'
                '<div class="info-text">'
                    '<p>'+ desc, '</p>'
                '</div>'
                '<div class="info-bottom">'
                    '<a href='+ new.get('link_site'),' class="info-author">'+ new.get('origin_author'), '</a>'
                    '<p>'+ str(published_time.strftime('%H:%M %d.%m.%Y ')), '</p>'
                '</div>'
                '<div class="button-wrap">'
                    '<a class="atuin-btn" href='+ new.get('link'),'>Подробнее</a>'
                '</div>'
            '</div>'
        '</article>')

print(x)

print("""</section></body>
</html>""")

