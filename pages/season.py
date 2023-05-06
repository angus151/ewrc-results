import datetime
import os
import sys

import requests
from pyquery import PyQuery as pyQuery

from config import app
from models.event import Event
from services import championship_service
from services import nationality_service


def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def get_seasons():
    url = app.BASE_URL + "/" + get_current_filename() + "/"

    try:
        print(url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if response.status_code == 200:

        doc = pyQuery(response.text)

        output = list()

        try:
            header = doc('.justify-content-start').not_('.season-nat').not_('.season-sct').not_('.header-flags')
            badges = header.find('a.badge').items()

            for index, badge in enumerate(badges, start=1):
                season = int(badge.attr('href').split('/')[2])
                output.append(season)

            return output

        except Exception as e:
            print(str(e))
            return list()
    else:
        print("Page not available: " + url)


def insert_nationalities(season):
    url = app.BASE_URL + "/" + get_current_filename() + "/" + str(season) + "/"

    try:
        print(url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if response.status_code == 200:

        doc = pyQuery(response.text)

        header = doc('.justify-content-start.season-nat')
        badges = header.find('a.badge').items()

        for index, badge in enumerate(badges, start=1):
            code = badge.attr('href').split('/')[3].replace('?nat=', '')
            nationality = badge.text()
            nationality_dict = {
                'id': code,
                'name': nationality,
                'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now(),
                'deleted_at': None
            }

            nationality_service.replace_nationalities(tuple(nationality_dict.values()))
    else:
        print("Page not available: " + url)


def insert_championships(season, nationality_code):
    url = app.BASE_URL + "/" + get_current_filename() + "/" + str(season) + "/" + '?nat=' + str(nationality_code)

    try:
        print(url)
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if response.status_code == 200:

        doc = pyQuery(response.text)

        header = doc('.justify-content-start.season-sct')
        badges = header.find('.season-sct-item').find('a.badge').items()

        for index, badge in enumerate(badges, start=1):
            code = badge.attr('href').split('/')[3]
            championship_id = code.split('-')[0]
            championship = badge.text()
            championship_dict = {
                'id': championship_id,
                'code': code,
                'name': championship,
                'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now(),
                'deleted_at': None
            }

            championship_service.replace_championships(tuple(championship_dict.values()))
    else:
        print("Page not available: " + url)


def insert_events(start_season, championship):
    for season in range(start_season, datetime.datetime.now().year + 1):

        url = app.BASE_URL + "/" + get_current_filename() + "/" + str(season) + "/" + championship + "/"

        try:
            print(url)
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        if response.status_code == 200:

            doc = pyQuery(response.text)

            # Events
            events = doc.items(".season-event")
            for index, event in enumerate(events, start=1):
                rally = Event()
                rally.save(season, event, index)
        else:
            print("Page not available: " + url)
