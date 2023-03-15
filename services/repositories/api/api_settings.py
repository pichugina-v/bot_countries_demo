import os

from dotenv import load_dotenv

load_dotenv()


WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
GEOCODER_URL = os.getenv('GEOCODER_URL')
