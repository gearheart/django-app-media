import os.path
from django.utils.importlib import import_module

def app_media_path(app_path, media, check_exists=True):
    """
    Return absolute path to given media for given app.
    """
    app_module = import_module(app_path)
    app_dir = os.path.dirname(app_module.__file__)
    app_media = os.path.realpath(os.path.join(app_dir, 'media', media))

    if check_exists and not os.path.exists(app_media):
        raise Exception("app_media_path: file doesn't exist: %s, %s'" % (
            app_path,
            media,
        ))
    return app_media

