import logging
from django.core.cache import cache

logger = logging.getLogger('custom')

def get_cached_data(key):
    data = cache.get(key)
    if data:
        logger.info(f"Cache hit for key: {key}")
    else:
        logger.warning(f"Cache miss for key: {key}")
    return data
