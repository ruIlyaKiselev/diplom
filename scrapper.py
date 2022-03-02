import re

import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://pddclub.ru/voditelskoe-udostoverenie-f4.html'
BASE_URL = 'https://pddclub.ru'
ADDITIONAL_URL = '/raznye-voprosy-f16'
END_URL = '.html'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33',
    'accept': '*/*'
}
FILE_NAME = 'questions.csv'


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([
                item['title'],
                item['link'],
                item['createdAt'],
                item['updatedAt'],
                item['posts'],
                item['views']
            ])


def get_html(url, params=None):
    r = requests.get(
        url=url,
        headers=HEADERS,
        params=params
    )
    return r


def get_list_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination_items = soup.findAll('div', class_='pagination')
    return int(pagination_items[0].findAll('a')[-1].text)


def get_details_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination_items = soup.findAll('div', class_='pagination')
    return int(pagination_items[0].findAll('a')[-1].text)


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        items = soup.findAll('ul', class_='topiclist topics')[1].findAll('li')
        links_list = []

        for item in items:
            links_list.append({
                'title': item.find('dt').find('a').text,
                'link': item.find('dt').find('a').get('href'),
                'createdAt': re.search("» (.*?)\r\n", item.find('dt').find('div', class_='h599').text).group(1),
                'updatedAt': re.search("\n (.*?)", item.find('dd', class_='lastpost').find('span').text).group(1),
                'posts': item.find('dd', class_='posts').text,
                'views': item.find('dd', class_='views').text
            })

        del links_list[0]
        return links_list
    except Exception:
        print('Error')


def parse_pages():
    html = get_html(BASE_URL + ADDITIONAL_URL + END_URL)

    if html.status_code == 200:
        items = []

        pages_count = get_list_pages_count(html.text)
        print(f'processing page: {0} total: {pages_count}')
        html = get_html(BASE_URL + ADDITIONAL_URL + END_URL)
        items.extend(get_links(html.text))

        for page in range(1, pages_count - 1):
            print(f'processing page: {page} total: {pages_count}')
            html = get_html(f'{BASE_URL}{ADDITIONAL_URL}-{page*25}{END_URL}')
            items.extend(get_links(html.text))
        print(f'received {len(items)} objects')
        save_file(items, FILE_NAME)
    else:
        print("Error!")


def get_details(url):
    html = get_html(url)

    if html.status_code == 200:
        items = []

        pages_count = get_details_pages_count(html.text)

