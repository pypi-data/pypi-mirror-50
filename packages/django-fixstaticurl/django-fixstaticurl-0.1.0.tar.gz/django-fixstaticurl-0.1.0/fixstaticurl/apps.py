from django.apps import AppConfig
from django.templatetags import static as _static_module
from django.templatetags.static import static as _system_static
from django.templatetags.static import do_static as _system_do_static
from django_global_request.middleware import get_request

def _static(*args, **kwargs):
    request = get_request()
    return request.META["SCRIPT_NAME"] + _system_static(*args, **kwargs)

def _do_static(*args, **kwargs):
    request = get_request()
    return request.META["SCRIPT_NAME"] + _system_do_static(*args, **kwargs)

class FixstaticurlConfig(AppConfig):
    name = 'fixstaticurl'

    def ready(self):
        setattr(_static_module, "static", _static)
        setattr(_static_module, "do_static", _do_static)
