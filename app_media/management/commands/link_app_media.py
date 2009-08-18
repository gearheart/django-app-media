import os
import sys
from django.conf import settings
from django.core.management.color import color_style
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-e', '--exclude',
            dest='exclude', action='append', default=[],
            help='App to exclude (you can use it multiple times).'),
    )
    help = 'Symlinks application media directories to MEDIA_ROOT.'
    args = '[appname ...]'

    def handle(self, *app_labels, **options):
        exclude = options.get('exclude', [])
        verbosity = options.get('verbosity', 0)

        if app_labels:
            def app_path(label):
                for app in settings.INSTALLED_APPS:
                     if a.split('.')[-1] == label:
                        return app
                raise CommandError('%s is not in INSTALLED_APPS' % label)
            app_list = map(app_path, app_labels)
        else:
            app_list = [a for a in settings.INSTALLED_APPS if not a in exclude]

        for app in app_list:
            link_app_media(app, verbosity)


# Almost completely took from
# http://www.arnebrodowski.de/blog/distributing-mediafiles-with-django-apps.html

def link_app_media(app_label, verbosity, **kwargs):
    """
    Looks if app has 'media' directory.
    If it has - this directory is then symlinked to the ``MEDIA_ROOT``
    directory, if it doesn't already exist.

    The symlink will not be created if a resource with the destination name
    already exists.
    """
    app_name = app_path.split('.')[-1]
    app_module = import_module(app_path)
    app_dir = os.path.dirname(app_module.__file__)
    app_media = os.path.join(app_dir, 'media')

    if os.path.exists(app_media):
        APP_MEDIA_DIR = getattr(settings, 'APP_MEDIA_DIR',
                os.path.join(settings.MEDIA_ROOT, 'apps'))
        dest = os.path.join(APP_MEDIA_DIR, app_name)
    if not os.path.exists(dest):
        try:
            os.symlink(app_media, dest) # will not work on windows.
            if verbosity > 1:
                print "symlinked app_media dir for app: %s" % app_name
        except:
            # windows users should get a note, that they should copy the
            # media files to the destination.
            error_msg = "Failed to link media for '%s'\n" % app_name
            instruction = ("Please copy the media files to the MEDIA_ROOT",
                "manually\n")
            sys.stderr.write(color_style().ERROR(str(error_msg)))
            sys.stderr.write(" ".join(instruction))
