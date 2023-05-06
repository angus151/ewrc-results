import os
import sqlite3
import sys

import requests
from pyquery import PyQuery as pyQuery

import definitions
from config import app
from models.driver import Driver
from services import driver_service


def get_current_filename():
	return os.path.splitext(os.path.basename(__file__))[0]


def insert_drivers(driver_list):
	for driver_id in driver_list:

		url = app.BASE_URL + "/" + get_current_filename() + "/" + str(driver_id)

		try:
			print(url)
			response = requests.get(url)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		if response.status_code == 200:

			doc = pyQuery(response.text)

			if doc("main > div").eq(0).hasClass("profile"):

				# Header - Driver Info
				driver = Driver(doc, driver_id)
				driver_service.insert_drivers(driver.get_tuple())
		else:
			print("Page not found: " + url)
