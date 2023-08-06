# -*- coding: utf-8 -*-
"""Main module."""
import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

_declination_months = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December',
}


class _Logger:
    def send_info(self, message):
        print('INFO: ' + message)

    def send_warning(self, message):
        print('WARNING: ' + message)

    def send_error(self, message):
        print('ERROR: ' + message)


class RabotaOtzyvyRu:
    BASE_URL = 'https://rabotaotzyvy.ru/'
    reviews = []

    def __init__(self, slug, logger=_Logger()):
        self.slug = slug
        self.logger = logger
        self.session = requests.Session()

    def start(self):
        self.request('GET', urljoin(self.BASE_URL, '{}.html'.format(self.slug)))
        self.reviews = list(self._collect_reviews())

    def _collect_reviews(self):
        """TODO: собрать комментраи над отзывами"""
        reviews_soup = self.soup.select('ol.comment-list>li.ticket-comment')
        if not reviews_soup:
            self.logger.send_warning('Reviews not found')
        for review_soup in reviews_soup:
            new_review = Review()
            new_review.id = int(review_soup['data-id'])
            new_review.text = review_soup.select_one(
                                                'div.ticket-comment-text>p').text
            date_string = review_soup.select_one(
                                        'span.ticket-comment-createdon').text
            new_review.date = self._convert_date(date_string)
            author = Author()
            author.name = review_soup.select_one(
                'div.ticket-comment-body.ticket-comment-guest'
                '>div.ticket-comment-header>span.ticket-comment-author').text
            new_review.author = author
            yield new_review

    @staticmethod
    def _convert_date(date_string):
        try:
            month_string = date_string[3:-5]
            month = _declination_months[month_string]
            return datetime.datetime.strptime(
                        date_string.replace(month_string, month),
                        '%d %B %Y').date()
        except KeyError:
            return None

    def request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        if not response.status_code == 200:
            self.logger.send_error(response.text)
            raise Exception("{}: {}".format(response.status_code,
                                            response.text))

        self.soup = BeautifulSoup(response.text, 'html.parser')
        return self.soup


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
        self.id = None
        self.text = ''
        self.date = None
        self.author = Author()
        self.sub_reviews = []

    def get_text(self):
        return self.text

    def get_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date,
            'author': self.author.get_dict(),
            'sub_reviews': [i.get_dict() for i in self.sub_reviews],
        }


if __name__ == '__main__':
    prov = RabotaOtzyvyRu('yandex-taxi-moskva-otzyvy-voditeley')
    prov.start()
    for review in prov.reviews:
        print(review.get_dict())
