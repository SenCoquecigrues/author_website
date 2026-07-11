import environ
from os import path

from django.conf import settings

def author_settings(request):
    if settings.DEBUG:
        environ.Env.read_env(path.join(settings.BASE_DIR, '.env'))

    env = environ.Env(
        AUTHOR_NAME=(str, 'My Name'),
        AUTHOR_BLURB=(str, 'My Name, grande autrice'),
        PAGE_TAGS=(str, 'autrice, romans, nouvelles'),
        META_DESCRIPTION=(str, 'Ici, de la grande littérature')
    )

    return {
        "AUTHOR_NAME": env('AUTHOR_NAME'),
        "AUTHOR_BLURB": env('AUTHOR_BLURB'),
        "PAGE_TAGS": env('PAGE_TAGS'),
        "META_DESCRIPTION": env('META_DESCRIPTION')
    }