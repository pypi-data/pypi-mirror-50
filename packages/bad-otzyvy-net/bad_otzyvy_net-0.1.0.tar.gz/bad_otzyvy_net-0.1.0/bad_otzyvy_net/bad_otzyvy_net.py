# -*- coding: utf-8 -*-

"""Main module."""
import re
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


class BadOtzyvyNet:
    rating = None
    BASE_URL = 'https://bad-otzyvy.net'
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
        resp = self.session.get(urljoin(self.BASE_URL, self.slug) + '.html')
        if not resp.status_code == 200:
            self.logger.send_error(resp.text)
            raise Exception(resp.text)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        self.rating.average_rating = int(
            soup.select_one('div.trusting>p.trustings>span').text[:-1]
        )
        self.id = self._convert_string_to_int(
            soup.find('meta', property='og:url')['content'])
        self.reviews = list(self._collect_reviews())
        self.logger.send_info('scrubber is finished')
        return self

    def _collect_reviews(self):
        page = 1
        while True:
            soup = self._get_page(page)
            for review_soup in soup.find_all('div', id='comment'):
                new_review = Review()
                new_review.text = review_soup.find(
                    'div', id=re.compile('comm-id-\d+')).text
                new_review.date = review_soup.select_one('p.dtreviewed').text
                new_review.author.name = review_soup\
                    .select_one('span.reviewer').text
                if review_soup.find('div', class_=['bad']):
                    new_review.status = _StatusReview.positive
                else:
                    new_review.status = _StatusReview.negative
                yield new_review
            else:
                break

    def _get_page(self, page):
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


class _StatusReview(Enum):
    negative = True
    positive = True


class Rating:
    average_rating = None
    min_scale = 0.0
    max_scale = 5.0

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
    prov = BadOtzyvyNet('5121-mtt-otzyvy')
    prov.start()
    for r in prov.reviews:
        print(r.get_dict())
