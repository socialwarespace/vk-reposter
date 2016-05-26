# -- coding: utf-8 --
import hashlib
from django.db import models
from django.utils import timezone
from django.conf import settings
from constance import config
try:
    from urllib import parse
except ImportError:
    import urlparse as parse


class Public(models.Model):
    """
    Модель хранит список пабликов, которые необходимо анализировать
    """
    domain = models.URLField(u'Адрес паблика', unique=True)
    subscriber_count = models.IntegerField(u'Количество подписчиков', default=0)
    last_parse = models.DateTimeField(u'Время последнего парса',
                                      blank=True, null=True)

    class Meta:
        verbose_name = u'Паблик'
        verbose_name_plural = u'Паблики'

    @property
    def public_name(self):
        return parse.urlparse(self.domain).path[1:]

    def __str__(self):
        return self.domain


class Post(models.Model):
    """
    Модель хранит посты пабликов
    """
    public = models.ForeignKey(Public)
    vk_id = models.IntegerField(u'ID поста вконтакте')
    owner_id = models.IntegerField(u'ID владельца поста')
    text = models.TextField(u'Текст поста')
    text_md5 = models.SlugField(u'MD5 сообщения', unique=True)
    like_count = models.IntegerField(u'Количество лайков')
    repost_count = models.IntegerField(u'Количество репостов')
    subscriber_count = models.IntegerField(u'Количество подписчиков группы')
    publication_time = models.DateTimeField(u'Время публикации')
    is_repost = models.BooleanField(u'Репост сделан', default=False)

    class Meta:
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'
        unique_together = ('public', 'vk_id')

    def __init__(self, *args, **kwargs):
        if kwargs:
            if isinstance(kwargs['publication_time'], int):
                # конвертируем timestamp в datetime
                time = timezone.datetime.fromtimestamp(
                    kwargs['publication_time']
                )
                kwargs['publication_time'] = timezone.make_aware(
                    time, timezone.get_current_timezone()
                )

        super(Post, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.text_md5 = hashlib.md5(self.text.encode()).hexdigest()
        super(Post, self).save(**kwargs)

    @property
    def rating(self):
        """ Возвращает рейтинг для объекта
        :return: integer
        """
        kwargs = {
            's': self.subscriber_count or 0.001,
            'r': self.repost_count or 0.001,
            'l': self.like_count or 0.001,
            't': self.hour_cont_from_publication(),
        }

        rating = eval(config.VK_RATING_FORMULA, kwargs)
        return int(rating)

    def hour_cont_from_publication(self):
        """ Возвращает количество часов с момента публикации.
        Округляет до 1, если меньше 1.
        :return: integer
        """
        delta = timezone.now() - self.publication_time

        return int(delta.total_seconds() / 60 / 60) + 1

    @property
    def vk_obj_uri(self):
        """ Возвращает uri поста вконтакте
        :return: string
        """
        return 'wall{0}_{1}'.format(self.owner_id, self.vk_id)

    @property
    def post_url(self):
        """ Возвращает url адрес поста
        :return: string
        """
        return 'https://vk.com/{0}'.format(self.vk_obj_uri)