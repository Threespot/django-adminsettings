from django.template.loader import render_to_string

class BaseSetting(object):
    name = None
    db_value = None
    template = None
    weight = None

    def to_python(self):
        return self.db_value

    def render(self):
        return render_to_string(self.template, { 'obj': self })


class StringSetting(BaseSetting):
    def to_python(self):
        return str(self.db_value)


class CharSetting(BaseSetting):
    template = 'adminsettings/char.html'


class TextSetting(CharSetting):
    template = 'adminsettings/textarea.html'


class MultiSetting(BaseSetting):
    """
    Allows you to choose one or more of a series of choices.
    """
    choices = None

    def to_python(self):
        return list(self.db_value)


class SelectSetting(MultiSetting):
    template = 'adminsettings/select.html'


class RadioSetting(MultiSetting):
    template = 'adminsettings/radio.html'


class CheckboxSetting(MultiSetting):
    template = 'adminsettings/checkbox.html'