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
    
    class BookmarkInstanceAdmin(admin.ModelAdmin):
        list_display = ('url', 'description', 'saved', 'user',)
        fields = ('url', 'description', 'note', 'user', 'saved')
        raw_id_fields = ('user',)
    
    admin.site.register(BookmarkInstance, BookmarkInstanceAdmin)