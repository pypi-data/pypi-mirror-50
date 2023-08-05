# -*- coding: utf-8 -*-

"""Main module."""
import json
import time

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


class FlampRU:
    BASE_URL = 'https://flamp.ru'
    DEFAULT_BEARER = '2b93f266f6a4df2bb7a196bb76dca60181ea3b37'

    _headers = CaseInsensitiveDict({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel'
                      ' Mac OS X x.y; rv:10.0)'
                      ' Gecko/20100101 Firefox/10.0',
        'X-Application': 'Flamp4',
        'Origin': 'https://flamp.ru',
        'Authorization': 'Bearer ',
        'Accept': ';q=1;depth=0;scopes={};application/json',
        'Referer': 'https://flamp.ru/',
        'Accept-Encoding': 'gzip, deflate, br'
    })

    def __init__(self, slug, logger=_Logger(), bearer_token=None):
        self.slug = slug
        self.session = requests.Session()
        self.logger = logger
        if bearer_token is None:
            self._headers['Authorization'] += FlampRU.DEFAULT_BEARER
        else:
            self._headers['Authorization'] += bearer_token
        self.session.headers = self._headers

    def get_reviews(self):
        json_data = self._get_reviews('https://flamp.ru'
                                      '/api/2.0/filials/'
                                      '{}/reviews?limit=25'.format(self.slug))
        reviews_ = json_data['reviews']
        while True:
            if 'next_link' not in json_data:
                break
            json_data = self._get_reviews(json_data['next_link'])
            reviews_.extend(json_data['reviews'])

        for review_ in reviews_:
            new_review = Review()
            new_review.id = review_['id']
            new_review.url = review_['url']
            new_review.text = review_['text']
            new_review.rating = review_['rating']
            new_review.date = review_['date_created']
            new_review.is_expert = review_['is_expert']
            new_review.likes_score = review_['likes_score']
            new_review.share_count = review_['share_count']
            yield new_review

    def _get_reviews(self, link):
        time.sleep(1.2)
        response = self.session.get(link)
        if not response.status_code == 200:
            self.logger.send_error(response.text)
            raise Exception(response.text)
        data = json.loads(response.text)
        return data


class Review:
    id = None
    url = ''
    text = ''
    rating = 0
    date = ''
    likes_score = 0
    share_count = 0


if __name__ == '__main__':
    prov = FlampRU(70000001020106111)
    reviews = list(prov.get_reviews())
    for review in reviews:
        print(review.id, review.rating)
    print(len(reviews))
