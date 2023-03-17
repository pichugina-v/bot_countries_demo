import os

from dotenv import load_dotenv

load_dotenv()


TG_API_TOKEN = os.getenv('TG_API_TOKEN')
# Invalid chars for city or country name
INVALID_CHARS = set('!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~;№|')
