#coding: utf8
import feedparser
import unicodedata
from datetime import datetime
import cgi
import time




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
<body>""")
#'https://meduza.io/rss2/all', 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
rss_urls=[{'rss_link': 'https://meduza.io/rss2/all',
           'rss_name': 'Медуза'},
            {'rss_link': 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss',
           'rss_name': 'РБК Новости'},
            {'rss_link': 'https://ria.ru/export/rss2/archive/index.xml',
           'rss_name': 'РИА Новости'},
        {'rss_link': 'http://news.rambler.ru/rss/world/',
           'rss_name': 'Рамблер'}]
# for line in open("../data/urls.txt", "r").read().split("\n"):
#     rss_urls.append(lin

for url in rss_urls:
    parser = feedparser.parse(url.get('rss_link'))
    news = []

    for entry in parser.entries:
        new_title = unicodedata.normalize("NFKD", entry.title)
        new_description = unicodedata.normalize("NFKD", entry.description, )
        new_link = unicodedata.normalize("NFKD", entry.link)
        new_published = unicodedata.normalize("NFKD", entry.published)
        published_time = datetime.strptime(new_published, '%a, %d %b %Y %X %z')
        new_published =  str(published_time.strftime('%Y-%m-%d %X'))
        print('<div class="news"><h1>'+ new_title, '</h1>'
              '<p>'+ new_description, '</p>'
              '<p>Источник: '+ url.get('rss_name'), '</p>'
              '<a href='+ new_link,'>Подробнее</a>'
              '<p>'+ new_published, '</p></div>')


print("""</body>
</html>""")

