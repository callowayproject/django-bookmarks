from django.conf import settings

DEFAULT_SETTINGS = {
    'VERIFY_EXISTS': False,
    'USE_TAGGING': False,
    'ITEMS_PER_FEED': 20,
    'ABSOLUTE_URL_IS_BOOKMARK': True,
    'MULTIUSER': True,
    'UNIQUE_BOOKMARKS': True
}

DEFAULT_SETTINGS.update(getattr(settings, 'BOOKMARK_SETTINGS', {}))

globals().update(DEFAULT_SETTINGS)
