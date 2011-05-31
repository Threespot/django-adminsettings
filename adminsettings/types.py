import re
from django.template.loader import render_to_string

class BaseSetting(object):
    name = None
    default = None
    template = None
    weight = None
    db_value = None

    def __init__(self, db_value):
        self.db_value = db_value

    def render(self):
        return render_to_string(self.template, { 'setting': self })

    def to_python(self):
        return self.value

    @classmethod
    def key(cls):
        ret = cls.name and cls.name or cls.__class__.__name__
        ret = re.sub('(.)([A-Z][a-z]\ +)', r'\1_\2', ret)
        ret = re.sub('([a-z0-9])([A-Z])', r'\1_\2', ret)
        return ret.replace(' ', '_').upper()

    @property
    def value(self):
        if self.db_value:
            return self.db_value
        return self.default


class StringSetting(BaseSetting):
    def to_python(self):
        return str(self.value)


class CharSetting(BaseSetting):
    template = 'adminsettings/types/char.html'


class TextSetting(CharSetting):
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