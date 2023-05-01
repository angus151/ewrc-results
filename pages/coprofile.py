import os
import sqlite3
import sys

import requests
from pyquery import PyQuery as pq

import definitions
from config import app
from models.driver import Driver
from services import driver_service

def get_current_filename():
    return os.path.splitext(os.path.basename(__file__))[0]


def insert_codrivers(codriver_list):
    for codriver_id in codriver_list:

        url = app.BASE_URL + "/" + get_current_filename() + "/" + str(codriver_id)

        try:
            print(url)
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        if response.status_code == 200:

            doc = pq(response.text)

            if doc("main > div").eq(0).hasClass("profile"):
                # Header - Codriver Info
                codriver = Driver(doc, codriver_id)
                driver_service.insert_codrivers(codriver.get_tuple())
