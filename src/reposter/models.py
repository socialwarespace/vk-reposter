import hashlib
from urllib import parse

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
        return parse.urlparse(self.domain).path[1:]

    def __str__(self):
        return self.domain


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

        rating = eval(settings.RATING_FORMULA, kwargs)
        return int(rating)

    def hour_cont_from_publication(self):
        """ Возвращает количество часов с момента публикации.
        Округляет до 1, если меньше 1.
        :return: integer
        """
        delta = timezone.now() - self.publication_time

        return int(delta.total_seconds() / 60 / 60) + 1
