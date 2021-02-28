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
<body>
<section class="grid">
""")
#'https://meduza.io/rss2/all', 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
rss_urls=[
        {'rss_link': 'https://meduza.io/rss2/all',
           'rss_name': 'Медуза'},
        #     {'rss_link': 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss',
        #    'rss_name': 'РБК Новости'},
        #     {'rss_link': 'https://ria.ru/export/rss2/archive/index.xml',
        #    'rss_name': 'РИА Новости'},
        # {'rss_link': 'http://news.rambler.ru/rss/world/',
        #    'rss_name': 'Рамблер Новости'},
        # {'rss_link': 'https://lenta.ru/rss',
        #    'rss_name': 'Lenta.ru'}
          ]
# for line in open("../data/urls.txt", "r").read().split("\n"):
#     rss_urls.append(lin

news = []

for url in rss_urls:
    parser = feedparser.parse(url.get('rss_link'))


    for entry in parser.entries:
        new_published = unicodedata.normalize("NFKD", entry.published)
        published_time = datetime.strptime(new_published, '%a, %d %b %Y %X %z')
        img_href = ""
        if entry.enclosures:
            img_href = (entry.enclosures[0].get('href'))
        news.append({
            'title': unicodedata.normalize("NFKD", entry.title),
            'description': unicodedata.normalize("NFKD", entry.description, ),
            'origin_author': url.get('rss_name'),
            'link': unicodedata.normalize("NFKD", entry.link),
            'published': str(published_time.strftime('%Y-%m-%d %X')),
            'img_href': img_href
        })
        news.sort(key=lambda dictionary: dictionary['published'], reverse=True)

#news.sort(key=lambda dictionary: dictionary['published'], reverse=True)

for new in news:
    hidden = ""
    if new.get('img_href') == "":
        hidden = "hidden"
    else: hidden = "visible"
    print('<article class="grid-item">'
        '<div class="image">'
            '<img src='+ new.get('img_href'),' />'
        '</div>'
        '<div class="info">'
            '<h2>' + new.get('title'), '</h2>'
            '<div class="info-text">'
                '<p>'+ new.get('description'), '</p>'
            '</div>'
            '<div class="info-bottom">'
                '<p class="info-author">'+ new.get('origin_author'), '</p>'
                '<p>'+ new.get('published'), '</p>'
            '</div>'                                    
            '<div class="button-wrap">'
                '<a class="atuin-btn" href='+ new.get('link'),'>Подробнее</a>'
            '</div>'
        '</div>'
    '</article>')



print("""</section></body>
</html>""")

