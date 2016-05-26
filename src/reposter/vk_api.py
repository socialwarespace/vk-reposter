# -- coding: utf-8 --
import vk
import logging
from django.conf import settings
from constance import config


class VkApi(object):
    _api_version = '5.52'

    def __init__(self):
        if settings.DEBUG:
            vk.logger.setLevel(logging.DEBUG)

    def get_authorized_api(self):
        session = vk.AuthSession(
            app_id=config.VK_APP_ID, user_login=config.VK_USER_LOGIN,
            user_password=config.VK_USER_PASSWORD, scope=settings.VK_SCOPE
        )

        return vk.API(session, v=self._api_version)

    def get_api(self):
        session = vk.AuthSession()

        return vk.API(session, v=self._api_version)


vk_api = VkApi()
