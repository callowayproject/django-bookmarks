from django.conf.urls.defaults import *
from models import Bookmark
from forms import BookmarkInstanceForm, BookmarkInstanceEditForm
from feeds import (BookmarkFeed, UserBookmarkFeed, 
                    AtomBookmarkFeed, AtomUserBookmarkFeed)

urlpatterns = patterns('',
    url(r'^$', 'bookmarks.views.bookmarks', name="all_bookmarks"),
    url(r'^rss/$', BookmarkFeed(), name='rss_all_bookmarks'),
    url(r'^rss/(?P<username>.+)/$', UserBookmarkFeed(), name='rss_user_bookmarks'),
    url(r'^atom/$', AtomBookmarkFeed(), name='atom_all_bookmarks'),
    url(r'^atom/(?P<username>.+)/$', AtomUserBookmarkFeed(), name='atom_user_bookmarks'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view='bookmarks.views.bookmark_detail',
        name='bookmark_detail'),
    url(r'^your_bookmarks/$', 'bookmarks.views.your_bookmarks', name="your_bookmarks"),
    url(r'^add/$', 'bookmarks.views.add', name="add_bookmark"),
    url(r'^(\d+)/delete/$', 'bookmarks.views.delete', name="delete_bookmark_instance"),
    url(r'^(\d+)/edit/$', 'bookmarks.views.edit', name="edit_bookmark_instance"),    
    
    # for json
    url(r'^json/(?P<model_name>[\d\w]+)/$', 'bookmarks.serializers.bookmarks_json'),
    url(r'^json/(?P<model_name>[\d\w]+)/(?P<object_id>\d+)/$', 'bookmarks.serializers.bookmarks_json'),
    
    # for xml
    url(r'^xml/(?P<model_name>[\d\w]+)/$', 'bookmarks.serializers.bookmarks_xml'),
    url(r'^xml/(?P<model_name>[\d\w]+)/(?P<object_id>\d+)/$', 'bookmarks.serializers.bookmarks_xml'),
)
