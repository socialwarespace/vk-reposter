from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone

from vk.exceptions import VkException
from reposter.vk_api import api

from conf.app_celery import app
from reposter.models import Post, Public


@app.task(name='parse_posts')
def parse_posts():
    """ Запускает парс новых постов из пабликов
    :return:
    """
    for public in Public.objects.all():
        try:
            group = api.groups.getMembers(group_id=public.public_name, count=0)
            subscribers = group['count']
        except VkException:
            # если парсим не паблик группы, а пользовательский
            user = api.users.get(user_ids=public.public_name)[0]
            followers = api.users.getFollowers(user_id=user['uid'], count=0)
            subscribers = followers['count']

        public.subscriber_count = subscribers
        parse_new_posts(public)
        public.last_parse = timezone.now()
        public.save()


def parse_new_posts(public):
    """ Парсит новые посты из паблика
    :return:
    """
    offset = 0
    parsed_all_post = False
    posts = api.wall.get(domain=public.public_name,
                         count=settings.POST_COUNT,
                         offset=offset)

    while not parsed_all_post:
        parsed_all_post = save_posts_and_check_exist(public, posts)

        if not parsed_all_post:
            offset += settings.POST_COUNT
            posts = api.wall.get(domain=public.public_name,
                                 count=settings.POST_COUNT,
                                 offset=offset)
            if len(posts) < 2:
                # если вернулось меньше 2х элементов дошли до конца
                parsed_all_post = True


def save_posts_and_check_exist(public, posts):
    """ Сохраняем посты в БД, пока не наткнёмся на дубликат
    :param public: паблик
    :param posts: посты
    :return: bool нашли уже сохранённый пост
    """
    parsed_all_post = False
    for data in posts:
        if not isinstance(data, dict):
            # первый элемент обычно количество постов в группе
            continue

        post = Post(
            public=public, vk_id=data['id'], text=data['text'],
            like_count=data['likes']['count'],
            repost_count=data['reposts']['count'],
            subscriber_count=public.subscriber_count,
            publication_time=data['date']
        )

        if post.rating < settings.RATING_LIMIT:
            # пропускаем объявления с слишком высоким рейтингом
            try:
                Post.objects.get(public=public, vk_id=data['id'])
                # api возвращает объекты по порядку, если объект уже сохранён
                # в БД - дошли до последнего значит дальше пойдут уже
                # сохранённые объекты
                parsed_all_post = True
            except Post.DoesNotExist:
                try:
                    post.save()
                except IntegrityError:
                    pass

    return parsed_all_post
