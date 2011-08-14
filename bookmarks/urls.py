from django.conf.urls.defaults import *
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkInstanceForm, BookmarkInstanceEditForm

urlpatterns = patterns('',
    url(r'^$', 'bookmarks.views.bookmarks', name="all_bookmarks"),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view='bookmarks.views.bookmark_detail',
        name='bookmark_detail'),
    url(r'^your_bookmarks/$', 'bookmarks.views.your_bookmarks', name="your_bookmarks"),
    url(r'^add/$', 'bookmarks.views.add', name="add_bookmark"),
    url(r'^(\d+)/delete/$', 'bookmarks.views.delete', name="delete_bookmark_instance"),
    url(r'^(\d+)/edit/$', 'bookmarks.views.edit', name="edit_bookmark_instance"),    
    
    # ajax validation
    (r'^validate_add/$', 'ajax_validation.views.validate', 
        {'form_class': BookmarkInstanceForm, 
        'callback': lambda request, 
        *args, 
        **kwargs: {'user': request.user}}, 
        'bookmark_instance_form_validate'),
        
    # ajax validation
    (r'^validate_edit/$', 'ajax_validation.views.validate', 
        {'form_class': BookmarkInstanceEditForm, 
        'callback': lambda request, 
        *args, 
        **kwargs: {'user': request.user}}, 
        'bookmark_instance_edit_form_validate'),
)
