"""
A Bookmark is unique to a URL whereas a BookmarkInstance represents a
particular Bookmark saved by a particular person.

This not only enables more than one user to save the same URL as a
bookmark but allows for per-user tagging.
"""

from datetime import datetime
import urlparse

from django.db.models import permalink
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from settings import (VERIFY_EXISTS, USE_TAGGING, ABSOLUTE_URL_IS_BOOKMARK, 
                      UNIQUE_BOOKMARKS)

if USE_TAGGING:
    try:
        from tagging.fields import TagField
        from tagging.models import Tag
    except ImportError:
        raise ImproperlyConfigured("Django Tagging is not installed but is"
            " configured for use in Django Bookmarks.")


class Bookmark(models.Model):
    
    url = models.URLField(unique=UNIQUE_BOOKMARKS)
    description = models.CharField(
        _('description'), 
        max_length=100)
    slug = models.SlugField()
    note = models.TextField(
        _('note'), 
        blank=True)
    has_favicon = models.BooleanField(_('has favicon'))
    favicon_checked = models.DateTimeField(
        _('favicon checked'), 
        default=datetime.now)
    adder = models.ForeignKey(
        User,
        blank=True, 
        null=True,
        related_name="added_bookmarks", 
        verbose_name=_('adder'))
    added = models.DateTimeField(
        _('added'), 
        default=datetime.now)
    
    if USE_TAGGING:
        tags = TagField()
    else:
        tags = models.CharField(blank=True, default='', max_length=255)
    
    def get_favicon_url(self, force=False):
        """
        return the URL of the favicon (if it exists) for the site this
        bookmark is on other return None.
        
        If force=True, the URL will be calculated even if it doesn't
        exist.
        """
        if self.has_favicon or force:
            base_url = '%s://%s' % urlparse.urlsplit(self.url)[:2]
            favicon_url = urlparse.urljoin(base_url, 'favicon.ico')
            return favicon_url
        return None
    
    def all_tags(self, min_count=False):
        if USE_TAGGING:
            return Tag.objects.usage_for_model(
                BookmarkInstance, counts=False, min_count=None, 
                filters={'bookmark': self.id})
        else:
            return self.tags.split(',')
    
    def all_tags_with_counts(self, min_count=False):
        if USE_TAGGING:
            return Tag.objects.usage_for_model(
                BookmarkInstance, counts=True, min_count=None, 
                filters={'bookmark': self.id})
        else:
            return self.tags.split(',')
    
    def __unicode__(self):
        return self.url
    
    if ABSOLUTE_URL_IS_BOOKMARK:
        def get_absolute_url(self):
            return self.url
    else:
        @permalink
        def get_absolute_url(self):
            return ('bookmark_detail', None, {
                'year': self.added.year,
                'month': self.added.strftime('%b').lower(),
                'day': self.added.day,
                'slug': self.slug
            })
    
    class Meta:
        ordering = ('-added', )


class BookmarkInstance(models.Model):
    """
    This model is created regardless of the setting MULTIUSER to make it easy
    to enable without having to worry about database table creation.
    
    Its admin will not show, however, if MULTIUSER is False
    """
    url = models.URLField(unique=False)
    bookmark = models.ForeignKey(
        Bookmark, 
        related_name="saved_instances", 
        verbose_name=_('bookmark'))
    user = models.ForeignKey(
        User, 
        related_name="saved_bookmarks", 
        verbose_name=_('user'))
    saved = models.DateTimeField(
        _('saved'), 
        default=datetime.now)
    description = models.CharField(
        _('description'), 
        max_length=100)
    note = models.TextField(
        _('note'), 
        blank=True)
    
    def save(self, force_insert=False, force_update=False, edit=False, **kwargs):
        from django.template.defaultfilters import slugify
        if edit:
            super(BookmarkInstance, self).save(force_insert, True)
        else:
            try:
                bookmark = Bookmark.objects.get(url=self.url)
            except Bookmark.DoesNotExist:
                # has_favicon=False is temporary as the view for adding 
                # bookmarks will change it
                bookmark = Bookmark(
                    url=self.url, slug=slugify(self.description), 
                    description=self.description, note=self.note, 
                    has_favicon=False, adder=self.user)
                bookmark.save()
            self.bookmark = bookmark
            super(BookmarkInstance, self).save(force_insert, force_update)
    
    def delete(self):
        bookmark = self.bookmark
        super(BookmarkInstance, self).delete()
        if bookmark.saved_instances.all().count() == 0:
            bookmark.delete()
    
    def __unicode__(self):
        return _("%(bookmark)s for %(user)s") % {
            'bookmark':self.bookmark, 'user':self.user
        }
