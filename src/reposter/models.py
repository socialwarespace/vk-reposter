import hashlib
from urllib.parse import urlparse

from django.db import models
from django.utils import timezone
from django.conf import settings


class Public(models.Model):
    """
    Модель хранит список пабликов, которые необходимо анализировать
    """
    domain = models.URLField('Адрес паблика', unique=True)
    subscriber_count = models.IntegerField('Количество подписчиков', default=0)
    last_parse = models.DateTimeField('Время последнего парса',
                                      blank=True, null=True)

    class Meta:
        verbose_name = 'Паблик'
        verbose_name_plural = 'Паблики'

    @property
    def public_name(self):
        return urlparse(self.domain).path[1:]


class Post(models.Model):
    """
    Модель хранит посты пабликов
    """
    public = models.ForeignKey(Public)
    vk_id = models.IntegerField('ID поста вконтакте')
    text = models.TextField('Текст поста')
    text_md5 = models.SlugField('MD5 сообщения', unique=True)
    like_count = models.IntegerField('Количество лайков')
    repost_count = models.IntegerField('Количество репостов')
    subscriber_count = models.IntegerField('Количество подписчиков группы')
    publication_time = models.DateTimeField('Время публикации')
    is_repost = models.BooleanField('Репост сделан', default=False)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        unique_together = ('public', 'vk_id')

    def save(self, **kwargs):
        if isinstance(self.publication_time, int):
            # конвертируем timestamp в datetime
            time = timezone.datetime.fromtimestamp(self.publication_time)
            self.publication_time = timezone.make_aware(
                time, timezone.get_current_timezone()
            )

        self.text_md5 = hashlib.md5(self.text.encode())

        super(Post, self).save(**kwargs)

    def rating(self):
        """ Возвращает рейтинг для объекта
        :return: integer
        """
        rating = eval(settings.RATING_FORMULA, {
            's': self.subscriber_count,
            'r': self.repost_count,
            'l': self.like_count,
            't': self.hour_cont_from_publication(),
        })

        return rating

    def hour_cont_from_publication(self):
        """ Возвращает количество часов с момента публикации.
        Округляет до 1, если меньше 1.
        :return: integer
        """
        delta = timezone.datetime.now() - self.publication_time

        return int(delta.total_seconds() / 60 / 60) + 1
