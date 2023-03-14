import os

from dotenv import load_dotenv

load_dotenv()


WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')

WEATHER_API_URL = os.getenv('WEATHER_API_URL')
REST_COUNTRY_API_URL = os.getenv('REST_COUNTRY_API_URL')
