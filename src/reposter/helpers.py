from constance import config
from django.utils import timezone
from reposter.vk_api import vk_api

api = vk_api.get_api()


def get_post_obsolete_date():
    """ Возвращает время после которого считаем пост устаревшим
    :return: datetime
    """
    return timezone.now() - timezone.timedelta(hours=config.VK_POST_OBSOLETE)


def get_group_id(group_name_or_id):
    group = api.groups.getById(group_id=group_name_or_id)[0]
    return group['id']
