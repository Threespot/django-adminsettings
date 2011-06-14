import re
from django.template.loader import render_to_string

class BaseSetting(object):
    name = None
    default = None
    display_default = False
    template = None
    weight = None
    db_value = None
    help_text = None

    def __init__(self, db_value):
        if db_value != self.default:
            self.db_value = db_value

    def render(self):
        return render_to_string(self.template, { 'setting': self })

    def to_python(self):
        return self.value

    def is_null(self):
        return False

    @classmethod
    def key(cls):
        ret = re.sub('(.)([A-Z][a-z]\ +)', r'\1_\2', cls.name)
        ret = re.sub('([a-z0-9])([A-Z])', r'\1_\2', ret)
        return ret.replace(' ', '_').upper()

    @property
    def value(self):
        if self.is_null():
            return self.db_value
        return self.default


class StringSetting(BaseSetting):
    def to_python(self):
        return str(self.value)

    def is_null(self):
        return self.db_value != ''


class CharSetting(StringSetting):
    template = 'adminsettings/types/char.html'


class TextSetting(StringSetting):
    template = 'adminsettings/types/textarea.html'


class MultiSetting(BaseSetting):
    """
    Allows you to choose one or more of a series of choices.
    """
    choices = None


class SelectSetting(MultiSetting):
    template = 'adminsettings/types/select.html'


class RadioSetting(MultiSetting):
    template = 'adminsettings/types/radio.html'


class CheckboxSetting(MultiSetting):
    template = 'adminsettings/types/checkbox.html'