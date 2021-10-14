import time
from tqdm import tqdm
import bs4
import requests
from bs4 import BeautifulSoup
import selenium
import re


def date_time_(article):
    date_time = article.find(class_="tm-article-snippet__datetime-published").time.attrs['datetime']
    date_time = date_time[:-5].split('T')
    date_time[0] = '{2}.{1}.{0}'.format(*[i for i in date_time[0].split('-')])
    date_time = ' '.join(date_time)
    return date_time


def tags_(article):
    tags = article.find_all(class_='tm-tags-list__link')
    tags = set(tag.text.strip() for tag in tags)
    return tags


def hubs_(article):
    hubs = article.find_all(class_='tm-hubs-list__link')
    hubs = set(hub.text.strip() for hub in hubs)
    return hubs


def find_intersection(site, tags, hubs, body, article, art_link, result):
    pattern = r'[-+=,\[\]{}\(\).?!\s/]'
    if (set(KEYWORDS) & tags) or (set(KEYWORDS) & hubs) or (set(KEYWORDS) & set(re.split(pattern, body))):
        date_time = date_time_(article)
        title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h1').text
        result.append(f'{date_time} - {title} - {site + art_link}')
    return result


def find_artices(site, art_link='/ru/all/'):
    response = requests.get(site + art_link)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    article = soup.find_all('article')
    if len(article) == 1:
        article = article[0]
    return article


def print_artices_with_KEYWORDS():
    site = 'https://habr.com'
    result = ['\nСтатьи с ключевыми словами:']
    articles = find_artices(site)
    for article in tqdm(articles):
        art_link = article.find(class_='tm-article-snippet__title-link').attrs['href']
        article = find_artices(site, art_link)
        body = article.find(class_="tm-article-body").text
        tags = tags_(article)
        hubs = hubs_(article)
        result = find_intersection(site, tags, hubs, body, article, art_link, result)
    if len(result) > 1:
        [print(item) for item in result]
    else:
        print('Статей с ключевыми словами не найдено... ¯\_(ツ)_/¯')


# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Ваш код
if __name__ == '__main__':
    print_artices_with_KEYWORDS()
