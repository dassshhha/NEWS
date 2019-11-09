import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path


headers = {'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
           }
base_url = 'https://www.gazeta.ru/news/'
base_url2 = 'https://lenta.ru/rss/news'
base_url3 = 'http://txt.newsru.com/allnews/'
base_url4 = 'https://www.vesti.ru/news/'


def parse(base_url, headers):
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'news_main_inner'})
        with open(str('data/parsedNews.txt'), 'w', encoding="utf-8") as f:
            for div in divs:
                title = div.find('span', attrs={'itemprop': 'headline'})
                href = div.find('a', attrs={'itemprop': 'mainEntityOfPage url'})
                if title is not None and href is not None:
                    title = title.text
                    f.write('"' + title.strip() + '"' + ',' + '\n')


def parse2(base_url, headers):
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        items = soup.find_all('item')
        with open(str('data/parsedNews.txt'), 'a', encoding="utf-8") as f:
            for item in items:
                title = item.find('title')
                if title is not None:
                    title = title.text
                    f.write('"' + title.strip() + '"' + ',' + '\n')


def parse3(base_url, headers):
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        titles = soup.find_all('a', attrs={'class': 'index-news-title'})
        with open(str('data/parsedNews.txt'), 'a', encoding="utf-8") as f:
            for div in titles:
                if div is not None:
                    title = div.text
                    f.write('"' + title.strip() + '"' + ',' + '\n')


def parse4(base_url, headers):
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        titles = soup.find_all('h3', attrs={'class': 'b-item__title'})
        with open(str('data/parsedNews.txt'), 'a', encoding="utf-8") as f:
            for div in titles:
                if div is not None:
                    title = div.text
                    f.write('"' + title.strip() + '"' + ',' + '\n')


parse(base_url, headers)
parse2(base_url2, headers)
parse3(base_url3, headers)
parse4(base_url4, headers)
