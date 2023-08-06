# -*- coding: utf-8 -*-

"""Main module."""
import time
from urllib.parse import urljoin

import requests
from requests.structures import CaseInsensitiveDict


class _Logger:
    def send_info(self, message):
        print('INFO: ' + message)

    def send_warning(self, message):
        print('WARNING: ' + message)

    def send_error(self, message):
        print('ERROR: ' + message)


class IskalkoOtzyvyRu:
    BASE_URL = 'https://iskalko-otzyvy.ru'
    API_URL = '/wp-json/wp/v2/'
    id = 0
    reviews = []

    def __init__(self, slug, logger=_Logger()):
        self.session = requests.Session()
        self.logger = logger
        self.slug = slug
        headers = CaseInsensitiveDict({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel'
                          ' Mac OS X x.y; rv:10.0)'
                          ' Gecko/20100101 Firefox/10.0',
        })
        self.session.headers = headers

    def start(self):
        self.id = self._get_post_id()
        self.reviews = list(self._collect_reviews())
        return self

    def _collect_reviews(self):
        """TODO: get url of comment"""
        self.logger.send_info('collecting reviews is start')
        page_number = 1
        while True:
            page = self._get_page(page_number)
            if not page:
                self.logger.send_info('collecting reviews is finish')
                break

            for review in page:
                if not review['parent'] == 0:
                    continue
                new_review = Review()
                new_review.id = review['id']
                new_review.date = review['date']
                new_review.text = review['content']['rendered']

                author = Author()
                author.name = review['author_name']
                new_review.author = author
                yield new_review

            page_number += 1

    def _get_page(self, page=1):
        time.sleep(1)
        resp = self.session.get(
            urljoin(
                urljoin(self.BASE_URL, self.API_URL),
                'comments?post={}&page={}'.format(self.id, page)
            )
        )
        if not resp.status_code == 200:
            self.logger.send_error(resp.text)
            raise Exception(resp.text)
        self.logger.send_info('get page: {}'.format(page))
        return resp.json()

    def _get_post_id(self):
        resp = self.session.get(
            'https://iskalko-otzyvy.ru/wp-json/wp/v2/posts?search={}'.format(
                self.slug
            ))
        if not resp.status_code == 200:
            self.logger.send_error(resp.text)
            raise Exception(resp.text)
        data_json = resp.json()
        return data_json[0]['id']


class Author:
    name = ''

    def get_name(self):
        return self.name

    def get_dict(self):
        return {
            'name': self.name,
        }


class Review:

    def __init__(self):
        self.id = ''
        self.text = ''
        self.date = ''
        self.url = ''
        self.author = Author()

    def get_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date,
            'url': self.url,
            'author': self.author.get_dict(),
        }

    def __repr__(self):
        return '{}: <{}> - {}'.format(self.id, self.date, self.author.get_name())


if __name__ == '__main__':
    prov = IskalkoOtzyvyRu('altapatri.ru отзывы')
    prov.start()
    for i in prov.reviews:
        print(i.get_dict())
