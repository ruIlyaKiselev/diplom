import csv
import re
import uuid

import requests
from bs4 import BeautifulSoup

from csv_utils import CsvUtils
from question_from_site import QuestionFromSite

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33',
    'accept': '*/*'
}


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
                'id': "",
                'title': item.find('dt').find('a').text,
                'question': "",
                'link': item.find('dt').find('a').get('href'),
                'createdAt': re.search("» (.*?)\r\n", item.find('dt').find('div', class_='h599').text).group(1),
                'updatedAt': re.search("\n (.*?)", item.find('dd', class_='lastpost').find('span').text).group(1),
                'posts': item.find('dd', class_='posts').text,
                'views': item.find('dd', class_='views').text,
                'answers': ""
            })

        del links_list[0]
        return links_list
    except Exception:
        print('Error')


def get_details(html):
    soup = BeautifulSoup(html, 'html.parser')

    index = 0

    try:
        question_from_site = QuestionFromSite(
            str(uuid.uuid4()),
            "",
            "",
            "",
            "",
            []
        )

        items = soup.find('div', id='page-body').findAll('div', class_='postbody')

        for item in items:
            text_list = item.find('div', class_='content').text
            if index == 0:
                question_from_site.question = text_list
            else:
                question_from_site.answers_list.append(text_list)
            index += 1

        return question_from_site
    except Exception:
        print('Error')


def parse_pages(base_url, additional_url, end_url, filename):
    html = get_html(base_url + additional_url + end_url)

    if html.status_code == 200:
        items_to_save = []

        pages_count = get_list_pages_count(html.text)
        print(f'processing page: {0} total: {pages_count}')
        current_links = get_links(html.text)
        for current_link in current_links:
            current_url = current_link['link']
            details_html = get_html(current_url)
            details = get_details(details_html.text)
            current_link['id'] = details.question_id
            current_link['question'] = details.question
            current_link['answers'] = details.answers_list.__str__()

        items_to_save.extend(current_links)

        for page in range(1, pages_count - 1):
            print(f'processing page: {page} total: {pages_count}')
            html = get_html(f'{base_url}{additional_url}-{page*25}{end_url}')
            current_links = get_links(html.text)
            for current_link in current_links:
                current_url = current_link['link']
                details_html = get_html(current_url)
                details = get_details(details_html.text)
                current_link['id'] = details.question_id
                current_link['question'] = details.question
                current_link['answers'] = details.answers_list.__str__()

            items_to_save.extend(current_links)

        print(f'received {len(items_to_save)} objects')
        CsvUtils.save_question_from_site(items_to_save, filename)
        return items_to_save
    else:
        print("Error!")


def parse_details(url):
    html = get_html(url)

    if html.status_code == 200:
        # pages_count = get_details_pages_count(html.text)
        # print(pages_count)
        details = get_details(html.text)
        print(details)
