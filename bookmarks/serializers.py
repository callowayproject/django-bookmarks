from django.core import serializers
from django.db.models.loading import get_model
from django.http import HttpResponse


def bookmarks_serialized(request, model_name, format, object_id=None):
    """
    Return a serialized response.
    """
    items = get_model("bookmarks", model_name).objects.all()
    if object_id is None:
        data = serializers.serialize(format, items)
    else:
        item = items.filter(id=object_id)
        data = serializers.serialize(format, item)
    return HttpResponse(data, mimetype="application/javascript")


def bookmarks_json(request, model_name, object_id=None):
    return bookmarks_serialized(request, model_name, "json", object_id)


def bookmarks_xml(request, model_name, object_id=None):
    return bookmarks_serialized(request, model_name, "xml", object_id)
