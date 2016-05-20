import vk
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone

from conf.app_celery import app
from reposter.models import Post, Public


@app.task(name='parse_posts')
def parse_posts():
    """ Запускает парс новых постов из пабликов
    :return:
    """
    for public in Public.objects.all():
        api = get_vk_api()
        group = api.groups.getMembers(group_id=public.public_name, count=0)

        public.subscriber_count = group['count']
        save_new_posts(public)
        public.last_parse = timezone.now()
        public.save()


def save_new_posts(public):
    """ Парсит новые посты из паблика
    :return:
    """
    api = get_vk_api()
    offset = 0
    posts = api.wall.get(domain=public.public_name, count=settings.POST_COUNT,
                         offset=offset)
    del posts[0]
    parsed_all_post = False
    while not parsed_all_post
    # запрашиваем посты



def save_and_check_exist_posts(public, posts):
    """ Сохраняем посты в БД, проверяя что бы сохраняемых постов уже не было в БД
    :param public: паблик
    :param posts: посты
    :return: bool нашли уже сохранённый пост
    """
    for p in posts:
        post = Post(
            public=public, vk_id=p['id'], text=p['text'],
            like_count=p['likes']['count'], repost_count=['reposts']['count'],
            subscriber_count=public.subscriber_count,
            publication_time=p['date']
        )
        if post.rating() < settings.RATING_LIMIT:
            # пропускаем объявления с слишком высоким рейтингом
            try:
                Post.objects.get(public=public, vk_id=p['id'])
                # api возвращает объекты по порядку, если объект уже сохранён
                # в БД - дошли до последнего значит дальше пойдут уже
                # сохранённые объекты
                return True
            except Post.DoesNotExist:
                try:
                    post.save()
                except IntegrityError:
                    pass

        return False


def get_vk_api():
    session = vk.Session()
    api = vk.API(session)

    return api
