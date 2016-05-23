import vk
import logging
from django.conf import settings


if settings.DEBUG:
    vk.logger.setLevel(logging.DEBUG)

session = vk.Session()
api = vk.API(session)
