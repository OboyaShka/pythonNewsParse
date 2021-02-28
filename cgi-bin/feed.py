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

rss_urls=[
        {  'rss_link': 'https://meduza.io/rss2/all',
           'rss_name': 'Медуза',
           'site_link': 'https://meduza.io/'},
            {'rss_link': 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss',
           'rss_name': 'РБК Новости',
            'site_link': 'https://www.rbc.ru/'},
            {'rss_link': 'https://ria.ru/export/rss2/archive/index.xml',
           'rss_name': 'РИА Новости',
             'site_link': 'https://ria.ru/'},
        {'rss_link': 'http://news.rambler.ru/rss/world/',
           'rss_name': 'Рамблер Новости',
         'site_link': 'https://news.rambler.ru/'},
        {'rss_link': 'https://lenta.ru/rss',
           'rss_name': 'Lenta.ru',
         'site_link': 'https://lenta.ru/'},
        {'rss_link': 'http://www.itar-tass.com/rss/all.xml',
           'rss_name': 'ТАСС',
         'site_link': 'https://tass.ru'},
          ]

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
            'link_site': url.get('site_link'),
            'published': str(published_time.strftime('%Y-%m-%d %H:%M')),
            'img_href': img_href
        })
        news.sort(key=lambda dictionary: dictionary['published'], reverse=True)

for new in news:
    if new.get('img_href').endswith('.jpg'):
        image_url = new.get('img_href')
    else:
        image_url = "../images/novosti.jpg"
    published_time = datetime.strptime(new.get('published'), '%Y-%m-%d %H:%M')


    print('<article class="grid-item">'
        '<div class="image">'
            '<img src='+ image_url,' />'
        '</div>'
        '<div class="info">'
            '<h2>' + new.get('title'), '</h2>'
            '<div class="info-text">'
                '<p>'+ new.get('description'), '</p>'
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



print("""</section></body>
</html>""")

