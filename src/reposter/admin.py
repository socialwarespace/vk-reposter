# -- coding: utf-8 --
from django.contrib import admin
from reposter.models import Public, Post


class PublicAdmin(admin.ModelAdmin):
    list_display = ('domain', 'last_parse')
    search_fields = ('domain', )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'vk_id', 'get_public_url', 'get_post_url', 'like_count',
        'repost_count', 'publication_time', 'repost_time', 'is_repost',
        'rating'
    )
    readonly_fields = ('rating', 'post_url')
    search_fields = ('vk_id', )

    def get_post_url(self, obj):
        return '<a href="{0}" target="_blank">{0}</a>'.format(obj.post_url)
    get_post_url.short_description = u'Адрес поста'
    get_post_url.allow_tags = True

    def get_public_url(self, obj):
        return '<a href="{0}" target="_blank">{0}</a>'.format(obj.public)
    get_public_url.short_description = u'Паблик'
    get_public_url.allow_tags = True


admin.site.register(Public, PublicAdmin)
admin.site.register(Post, PostAdmin)
