import os

from dotenv import load_dotenv

load_dotenv()


GEOCODER_URL = os.getenv('GEOCODER_URL')
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

COUNTRY_INFO_URL = os.environ['COUNTRY_INFO_URL']
WEATHER_INFO_URL = os.environ['WEATHER_INFO_URL']
CURRENCY_INFO_URL = os.environ['CURRENCY_INFO_URL']
