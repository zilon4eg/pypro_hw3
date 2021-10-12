import time
from tqdm import tqdm
import bs4
import requests
from bs4 import BeautifulSoup
import selenium
import re


# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Ваш код
site = 'https://habr.com'
response = requests.get(site + '/ru/all/')
response.raise_for_status()

soup = bs4.BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all('article')

result = ['Статьи с ключевыми словами:']

for article in tqdm(articles):
# for article in articles:

    art_link = article.find(class_='tm-article-snippet__title-link').attrs['href']

    response = requests.get(site + art_link)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    article = soup.find('article')

    body = article.find(class_="tm-article-body").text


    tags = article.find_all(class_='tm-tags-list__link')
    tags = set(tag.text.strip() for tag in tags)


    hubs = article.find_all(class_='tm-hubs-list__link')
    hubs = set(hub.text.strip() for hub in hubs)


    if (set(KEYWORDS) & tags) or (set(KEYWORDS) & hubs) or (set(KEYWORDS) & set(re.split('[-+=,\[\]{}\(\).?!\s/]', body))):
        date_time = article.find(class_="tm-article-snippet__datetime-published").time.attrs['datetime']
        date_time = date_time[:-5].split('T')
        date_time[0] = '{2}.{1}.{0}'.format(*[i for i in date_time[0].split('-')])
        date_time = ' '.join(date_time)
        title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h1').text
        result.append(f'{date_time} - {title} - {site + art_link}')
if len(result) > 1:
    for item in result:
        print(item)
else:
    print('Статей с ключевыми словами не найдено... ¯\_(ツ)_/¯')