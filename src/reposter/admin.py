from django.contrib import admin
from reposter.models import Public, Post


class PublicAdmin(admin.ModelAdmin):
    list_display = ('domain', 'last_parse')
    search_fields = ('domain', )


class PostAdmin(admin.ModelAdmin):
    list_display = ('vk_id', 'public', 'like_count', 'repost_count',
                    'subscriber_count', 'publication_time', 'is_repost',
                    'rating')
    readonly_fields = ('rating', )
    search_fields = ('vk_id', )


admin.site.register(Public, PublicAdmin)
admin.site.register(Post, PostAdmin)
