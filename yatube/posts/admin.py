from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    """Detail admin side for manage of user posts."""
    list_display = ('pk', 'text', 'created', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('created',)
    list_editable = ('group',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
