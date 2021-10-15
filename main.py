import time
from tqdm import tqdm
import bs4
import requests
from bs4 import BeautifulSoup
import selenium
import re


def date_time_(article):
    '''
    Форматирует дату и время в удобный для чтения вид
    :param article: статья
    :return: дата/время в формате DD.MM.YYYY HH:MM:SS
    P.S. В задании указано вывести только дату, но при выводе, дата с указанием времени написания статьи, выглядит лучше
    Решил сделать так
    '''
    date_time = article.find(class_="tm-article-snippet__datetime-published").time.attrs['datetime']
    date_time = date_time[:-5].split('T')
    date_time[0] = '{2}.{1}.{0}'.format(*[i for i in date_time[0].split('-')])
    date_time = ' '.join(date_time)
    return date_time


def tags_(article):
    '''
    Ищет теги в статье и формирует из них множество
    :param article: статья
    :return: множество из тегов
    '''
    tags = article.find_all(class_='tm-tags-list__link')
    tags = set(tag.text.strip().lower() for tag in tags)
    return tags


def hubs_(article):
    '''
    Ищет "хабы" в статье и формирует из них множество
    :param article: статья
    :return: множество из "хабов"
    '''
    hubs = article.find_all(class_='tm-hubs-list__link')
    hubs = set(map(lambda i: i.text.strip().lower(), hubs))
    return hubs


def find_intersection(site, tags, hubs, body, article, art_link, result):
    '''
    Определяет наличие ключевых слов в статье. Если находит, добавляет дату/время, заголовок, ссылку в переменную result
    :param site: ссылка https://habr.com
    :param tags: тэги статьи
    :param hubs: "хабы" статьи
    :param body: текст статьи
    :param article: статья
    :param art_link: ссылка на статью
    :param result: переменная в которую функция добавляет дату/время написания статьи,
    заголовок статьи и ссылку на нее, если находит пересечение множеств для определения наличия искомых ключевых слов в
    тегах, "хабах", заголовке, теле статьи. Слова во всех множествах приводятся к нижнему
    :return: переменную result
    '''
    keywords = list(map(str.lower, KEYWORDS))
    title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h1').text
    pattern = r'\W'
    if set(keywords) & tags \
            or set(keywords) & hubs \
            or set(keywords) & set(re.split(pattern, body.lower())) \
            or set(keywords) & set(re.split(pattern, title.lower())):
        date_time = date_time_(article)
        result.append(f'{date_time} - {title} - {site + art_link}')
    return result


def find_artices(site, art_link='/ru/all/'):
    '''
    Проверяет доступность ресурса и получает статью или список статей
    :param site: ссылка https://habr.com
    :param art_link: ссылка на одну статью, либо на главную страницу https://habr.com (если аргумент отсутствует)
    :return: возвращает статью или список статей
    '''
    response = requests.get(site + art_link)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    article = soup.find_all('article')
    if len(article) == 1:
        article = article[0]
    return article


def print_artices_with_KEYWORDS():
    '''
    Ищет статьи на главной https://habr.com, проверяет наличие ключевых слов в каждой из них (в тегах, "хабах",
    заголовке, тексте). Выводит на экран дату/время, заголовок, ссылку статей с ключевыми словами. Либо сообщение
    об отсутствии статей.
    P.S. В задании четко не указано, поэтому поиск решил сделать нерегистрозависимым.
    '''
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
