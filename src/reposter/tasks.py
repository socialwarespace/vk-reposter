import vk
from django.conf import settings
from conf.app_celery import app
from reposter.models import Post, Public


@app.task(name='parse_posts')
def parse_posts():
    """ Запускает парс новых постов из пабликов
    :return:
    """
    for public in Public.objects.all():
        get_new_public_posts(public.domain)


def get_new_public_posts(domain):
    """ Парсит новые посты из паблика
    :return:
    """
    session = vk.Session()
    api = vk.API(session)
    posts = api.wall.get(domain=domain, count=settings.POST_COUNT)
