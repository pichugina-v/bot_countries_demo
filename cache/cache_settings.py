import os

import aioredis
from dotenv import load_dotenv

load_dotenv()


REDIS_URL = os.getenv('REDIS_URL')

REDIS = aioredis.from_url(REDIS_URL, decode_responses=True)
LIVE_CACHE_SECONDS = 3600
