from datetime import datetime
import urllib2

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import date_based

from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkInstanceForm, BookmarkInstanceEditForm
from settings import MULTIUSER

if MULTIUSER:
    from models import BookmarkInstance
    from forms import BookmarkInstanceEditForm

def bookmarks(request, template_name='bookmarks/bookmarks.html'):
    all_bookmarks = Bookmark.objects.all().order_by("-added")
    if request.user.is_authenticated():
        if MULTIUSER:
            user_bookmarks = BookmarkInstance.objects.filter(
                user=request.user)
        else:
            user_bookmarks = Bookmark.objects.filter(adder=request.user)
    else:
        user_bookmarks = []
    return render_to_response(template_name, {
        "bookmarks": all_bookmarks,
        "user_bookmarks": user_bookmarks,
    }, context_instance=RequestContext(request))


def bookmark_detail(request, slug, year, month, day, template_name='bookmarks/bookmark_detail.html', **kwargs):
    '''Detail bookmark view.'''

    return date_based.object_detail(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'added',
        slug = slug,
        queryset = Bookmark.objects.all(),
        template_object_name='bookmark',
        template_name=template_name,
        **kwargs
    )


@login_required
def your_bookmarks(request):
    if MULTIUSER:
        bookmark_instances = BookmarkInstance.objects.filter(user=request.user).order_by("-saved")
    else:
        bookmark_instances = Bookmark.objects.filter(adder=request.user).order_by("-added")
    
    return render_to_response("bookmarks/your_bookmarks.html", {
        "bookmark_instances": bookmark_instances,
    }, context_instance=RequestContext(request))

@login_required
def add(request):

    if request.method == "POST":
        bookmark_form = BookmarkInstanceForm(request.user, request.POST)
        if bookmark_form.is_valid():
            bookmark_instance = bookmark_form.save(commit=False)
            bookmark_instance.user = request.user
            bookmark_instance.save()
            bookmark = bookmark_instance.bookmark

            try:
                headers = {
                    "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                    "Accept-Language" : "en-us,en;q=0.5",
                    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Connection" : "close",
                    ##"User-Agent": settings.URL_VALIDATOR_USER_AGENT
                    }
                req = urllib2.Request(bookmark.get_favicon_url(force=True), None, headers)
                u = urllib2.urlopen(req)
                has_favicon = True
            except:
                has_favicon = False

            bookmark.has_favicon = has_favicon
            bookmark.favicon_checked = datetime.now()
            bookmark.save()

            if bookmark_form.should_redirect():
                return HttpResponseRedirect(bookmark.url)
            else:
                request.user.message_set.create(message=_("You have saved bookmark '%(description)s'") % {'description': bookmark_instance.description})
                return HttpResponseRedirect(reverse("bookmarks.views.bookmarks"))
    else:
        initial = {}
        if "url" in request.GET:
            initial["url"] = request.GET["url"]
        if "description" in request.GET:
            initial["description"] = request.GET["description"].strip()
        if "redirect" in request.GET:
            initial["redirect"] = request.GET["redirect"]

        if initial:
            bookmark_form = BookmarkInstanceForm(initial=initial)
        else:
            bookmark_form = BookmarkInstanceForm()

    bookmarks_add_url = "http://" + Site.objects.get_current().domain + reverse(add)
    bookmarklet = "javascript:location.href='%s?url='+encodeURIComponent(location.href)+';description='+encodeURIComponent(document.title)+';redirect=on'" % bookmarks_add_url

    return render_to_response("bookmarks/add.html", {
        "bookmarklet": bookmarklet,
        "bookmark_form": bookmark_form,
    }, context_instance=RequestContext(request))

@login_required
def delete(request, bookmark_instance_id):

    bookmark_instance = get_object_or_404(BookmarkInstance, id=bookmark_instance_id)
    if request.user == bookmark_instance.user:
        bookmark_instance.delete()
        request.user.message_set.create(message="Bookmark Deleted")

    if "next" in request.GET:
        next = request.GET["next"]
    else:
        next = reverse("bookmarks.views.bookmarks")

    return HttpResponseRedirect(next)

@login_required
def edit(request, bookmark_instance_id):    
    bookmark_instance = get_object_or_404(BookmarkInstance, id=bookmark_instance_id)
    
    if request.method == "POST":
        bookmark_form = BookmarkInstanceEditForm(request.user, request.POST, instance=bookmark_instance)
        if bookmark_form.is_valid():
            bookmark_instance = bookmark_form.save(commit=False)
            bookmark_instance.user = request.user
            bookmark_instance.save(edit=True)

            
            if request.POST.get('redirect', None):
                return HttpResponseRedirect(bookmark_instance.bookmark.url)
            else:
                request.user.message_set.create(message=_("You have finished editing bookmark '%(description)s'") % {'description': bookmark_instance.description})
                return HttpResponseRedirect(reverse("bookmarks.views.your_bookmarks"))
    elif request.user == bookmark_instance.user:
        data = dict(      
            description=bookmark_instance.description,
            note=bookmark_instance.note,
            tags=bookmark_instance.tags
        )
        bookmark_form = BookmarkInstanceEditForm(initial=data) 

    bookmarks_add_url = "http://" + Site.objects.get_current().domain + reverse(add)
    bookmarklet = "javascript:location.href='%s?url='+encodeURIComponent(location.href)+';description='+encodeURIComponent(document.title)+';redirect=on'" % bookmarks_add_url

    return render_to_response("bookmarks/edit.html", {
        "bookmarklet": bookmarklet,
        "bookmark_form": bookmark_form,
    }, context_instance=RequestContext(request))        
