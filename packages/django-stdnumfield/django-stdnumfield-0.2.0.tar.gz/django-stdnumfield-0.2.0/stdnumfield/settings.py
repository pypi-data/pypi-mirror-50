from django.conf import settings

from stdnumfield import STDNUM_FORMATS


_DEFAULTS = {"DEFAULT_FORMATS": STDNUM_FORMATS.keys()}

_SETTINGS = getattr(settings, "STDNUMFIELD", {})


def _get(attribute):
    return _SETTINGS.get(attribute, _DEFAULTS[attribute])


DEFAULT_FORMATS = _get("DEFAULT_FORMATS")
