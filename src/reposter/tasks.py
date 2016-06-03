# -- coding: utf-8 --
import time

from celery.utils.log import get_task_logger
from constance import config
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
from vk.exceptions import VkException

from conf.app_celery import app
from reposter.helpers import get_post_obsolete_date, get_group_id
from reposter.models import Post, Public
from reposter.vk_api import vk_api

api = vk_api.get_api()


@app.task(name='repost_posts')
def repost_posts():
    """ Репост записей на стену
    :return:
    """
    auth_api = vk_api.get_authorized_api()

    # выбираем одну случайную запись для репоста, но не из группы,
    # которой постили в прошлый раз
    for_repost = Post.objects.filter(
        is_repost=False, publication_time__gte=get_post_obsolete_date()
    )
    try:
        last_repost = Post.objects.filter(is_repost=True).latest('repost_time')
    except Post.DoesNotExist:
        pass
    else:
        for_repost.exclude(public=last_repost.public)
    for_repost = [for_repost.order_by('?').first()]

    for post in for_repost:
        kwargs = {
            'object': post.vk_obj_uri,
            'message': config.VK_REPOST_MESSAGE,
        }
        if config.VK_REPOST_TO:
            kwargs['group_id'] = get_group_id(config.VK_REPOST_TO)

        try:
            time.sleep(settings.VK_API_INTERVAL)
            auth_api.wall.repost(**kwargs)
        except VkException:
            time.sleep(settings.VK_API_INTERVAL * 60)
            auth_api = vk_api.get_authorized_api()
            try:
                auth_api.wall.repost(**kwargs)
            except VkException:
                logger = get_task_logger(__name__)
                logger.info(
                    u'Превышен лимит на количество репостов (50 в день)'
                )
                return

        post.is_repost = True
        post.repost_time = timezone.now()
        post.save()


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
                         count=settings.VK_POST_COUNT,
                         offset=offset)

    while not parsed_all_post:
        parsed_all_post = save_posts_and_check_exist(public, posts['items'])

        if not parsed_all_post:
            offset += settings.VK_POST_COUNT
            time.sleep(settings.VK_API_INTERVAL)
            posts = api.wall.get(domain=public.public_name,
                                 count=settings.VK_POST_COUNT,
                                 offset=offset)
            if not posts['items']:
                # если нет элементов дошли до конца
                parsed_all_post = True


def save_posts_and_check_exist(public, posts):
    """ Сохраняем посты в БД, пока не наткнёмся на дубликат
    :param public: паблик
    :param posts: посты
    :return: bool нашли уже сохранённый пост
    """
    saved_post_count = 0

    for data in posts:
        post = Post(
            public=public,
            vk_id=data['id'],
            owner_id=data['owner_id'],
            text=data['text'],
            like_count=data['likes']['count'],
            repost_count=data['reposts']['count'],
            subscriber_count=public.subscriber_count,
            publication_time=data['date']
        )

        if post.publication_time < get_post_obsolete_date():
            # не обрабатываем посты с датой публикации больше суток
            continue

        if post.rating < config.VK_RATING_LIMIT:
            # пропускаем объявления с слишком высоким рейтингом
            try:
                post.save()
                saved_post_count += 1
            except IntegrityError:
                continue

    parsed_all_post = not bool(saved_post_count)
    return parsed_all_post
