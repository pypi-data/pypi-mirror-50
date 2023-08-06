# -*- coding: utf-8 -*-

"""Main module."""
import re
import time
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict


class _Logger:
    def send_info(self, message):
        print('INFO: ' + message)

    def send_warning(self, message):
        print('WARNING: ' + message)

    def send_error(self, message):
        print('ERROR: ' + message)


class NesovetyuCom:
    rating = None
    BASE_URL = 'https://nesovetyu.com'
    id = None
    reviews = []

    def __init__(self, slug, logger=_Logger):
        self.session = requests.Session()
        self.logger = logger()
        self.slug = str(slug)
        self.rating = Rating()
        self.session.headers = CaseInsensitiveDict({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel'
                          ' Mac OS X x.y; rv:10.0)'
                          ' Gecko/20100101 Firefox/10.0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'text/html; charset=utf-8'
        })

    def start(self):
        self.logger.send_info('scrubber is started')
        self.id = self._convert_string_to_int(self.slug)
        self.reviews = list(self._collect_reviews())
        self.logger.send_info('scrubber is finished')
        return self

    def _collect_reviews(self):
        page = 1
        while True:
            soup = self._get_page(page)
            page += 1
            if len(soup.find_all('div', class_=['hreview'])) == 0:
                break
            for review_soup in soup.find_all('div', class_=['hreview']):
                new_review = Review()
                new_review.text = review_soup.find(
                    'div', id=re.compile('comm-id-\d+')).text
                new_review.date = review_soup.find('div',
                                                   id=re.compile('comm-id-')).text
                new_review.author.name = review_soup\
                    .select_one('span.reviewer').text
                if 'Я работала... полгода...выдержала' in new_review.text:
                    print('hi')
                if review_soup['class'][0] == 'c-good':
                    new_review.rating.average_rating = 1
                else:
                    new_review.rating.average_rating = 0
                yield new_review

    def _get_page(self, page):
        time.sleep(0.9)
        self.logger.send_info('parse page: {}'.format(page))
        resp = self.session.get(urljoin(self.BASE_URL,
                                        '/engine/ajax/comments.php'
                                        '?cstart={page}'
                                        '&news_id={company_id}&skin=Default'
                                        .format(page=page, company_id=self.id)))
        if not resp.status_code == 200:
            self.logger.send_error(resp.text)
            raise Exception(resp.text)

        return BeautifulSoup(resp.json()['comments'], 'html.parser')

    @staticmethod
    def _convert_string_to_int(text):
        try:
            return int(text)
        except (ValueError, TypeError):
            return int(re.findall("\d+", text)[0])

    @staticmethod
    def _convert_string_to_float(text):
        text = text.replace(',', '.')
        try:
            return float(text)
        except ValueError:
            return float(re.findall("\d+\.\d+", text)[0])


class Rating:
    average_rating = None
    min_scale = 0
    max_scale = 1

    def get_dict(self):
        return {
            'average_rating': self.average_rating,
            'on_scale': self.min_scale,
            'max_scale': self.max_scale,
        }

    def __repr__(self):
        return '<{} из {}>'.format(self.average_rating, self.max_scale)


class Author:
    name = ''

    def get_name(self):
        return self.name

    def get_dict(self):
        return {
            'name': self.name
        }


class Review:
    def __init__(self):
        self.text = ''
        self.date = ''
        self.author = Author()
        self.status = None
        self.rating = Rating()

    def get_dict(self):
        return {
            'text': self.text,
            'date': self.date,
            'status': self.status,
            'rating': self.rating.get_dict(),
            'author': self.author.get_dict(),
        }

    def __repr__(self):
        return '<{}: {} -> {}'.format(self.date,
                                      self.author.get_name(), self.status)


if __name__ == '__main__':
    prov = NesovetyuCom('1998-ooo-nsv-otzyvy-sotrudnikov-nacionalnaya-sluzhba'
                        '-vzyskaniya-dolgov-otzyvy-rabotnikov')
    prov.start()
    for r in prov.reviews:
        print(r.get_dict())
    print(len(prov.reviews))
