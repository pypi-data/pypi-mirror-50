# -*- coding: utf-8 -*-

"""Main module."""
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class _Logger:
    def send_info(self, message):
        print('INFO: ' + message)

    def send_warning(self, message):
        print('WARNING: ' + message)

    def send_error(self, message):
        print('ERROR: ' + message)


class OtzyvyCo(object):
    BASE_URL = 'https://www.otzyvy.co'
    reviews = []
    show_count = 0
    count = 0
    logger = None

    def __init__(self, slug, logger=_Logger()):
        self.session = requests.Session()
        self.logger = logger
        self.slug = slug
        self.rating = Rating()

    def start(self):
        response = self.session.get(
            urljoin(self.BASE_URL, '/company/{}/feedbacks/'.format(self.slug)))
        if not response.status_code == 200:
            self.logger.send_error(response.text)
            raise Exception(response.text, response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        self.rating.average_rating = float(
            soup.select_one('div.vote-item.vote-count>span').text)
        for review_soup in soup.find_all('div', class_='comment-wrapper'):
            new_review = Review()
            new_review.id = self._convert_string_to_int(review_soup['id'])
            new_review.text = self._str(review_soup.find('div',
                                                         class_='text').text)
            new_review.author.name = self._str(review_soup.find(
                                    'li', class_='comment-author').text.strip())
            new_review.date = self._str(review_soup.find(
                                    'li', class_='comment-date').text)
            new_review.url = review_soup.select_one('li.comment-link>a')['href']
            self.reviews.append(new_review)
        return self

    @staticmethod
    def _str(text):
        return str(text).strip().replace('\n', '')

    @staticmethod
    def _convert_string_to_int(text):
        try:
            return int(text)
        except (ValueError, TypeError):
            return int(re.findall("\d+", text)[0])


class Rating:
    average_rating = None
    min_scale = None
    max_scale = None

    def get_dict(self):
        return {
            'average_rating': self.average_rating,
            'min_scale': self.min_scale,
            'on_scale': self.max_scale,
        }


class Author:
    name = ''

    def get_dict(self):
        return {
            'name': self.name,
        }


class Review:

    def __init__(self):
        self.rating = Rating()
        self.id = 0
        self.text = ''
        self.url = ''
        self.date = ''
        self.author = Author()

    def get_text(self):
        return self.text

    def get_dict(self):
        return {
            'id': self.id,
            'rating': self.rating.get_dict(),
            'url': self.url,
            'text': self.text,
            'date': self.date,
            'author': self.author.get_dict(),
        }

    def __str__(self):
        return self.text[:50]

    def __repr__(self):
        if len(self.text) >= 50:
            return self.text
        return self.text[:50] + '...'


if __name__ == '__main__':
    prov = OtzyvyCo('ae-salon')
    prov.start()

    for r in prov.reviews:
        print(r.get_dict())
    print(prov.rating.get_dict())
