from django.contrib import admin

from settings import MULTIUSER
from bookmarks.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('url', 'description', 'added', 'adder',)
    prepopulated_fields = {'slug': ('description',)}
    raw_id_fields = ('adder',)

admin.site.register(Bookmark, BookmarkAdmin)

if MULTIUSER:
    from bookmarks.models import BookmarkInstance
    admin.site.register(BookmarkInstance)