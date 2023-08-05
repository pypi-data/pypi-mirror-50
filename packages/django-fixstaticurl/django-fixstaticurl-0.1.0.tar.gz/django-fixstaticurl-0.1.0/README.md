# django-fixstaticurl

Django static tag ignores META.SCRIPT_NAME settings, so we get it fixed.


## Install

    pip install django-fixstaticurl


## Settings

1. Install and config django-middleware-global-request properly, see https://pypi.org/project/django-middleware-global-request/
1. Add fixstaticurl in settings.INSTALLED_APPS
1. Config nginx and uwsgi properly so that the META.SCRIPT_NAME is correct

