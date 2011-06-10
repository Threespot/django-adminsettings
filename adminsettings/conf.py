from django.contrib.contenttypes.generic import GenericStackedInline
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

from adminsettings.exceptions import AlreadyRegistered, NotRegistered
from adminsettings.models import AdminSetting

CACHE_NAME = 'adminsettings_cache'
CACHE_TTL = 10


class SettingValue(str):
    setting_object = None
    model_object = None


class AdminSettingSite(object):

    def __init__(self):
        self._registry = {}

    def __iter__(self):
        return self._registry.__iter__()

    def register(self, admin_setting, setting_cache=None):
        """
        Registers a given setting. If it has already been registered, this
        will raise AlreadyRegistered.
        """

        # To prevent multiple DB lookups, let's run and evaluate the queryset,
        # which allows us to pass on the value to any sub-registrations (i.e. if
        # a list was passed to the function)

        if not setting_cache:
            setting_cache = AdminSetting.objects.all()

        # Iterables containing setting objects can also be registered
        if hasattr(admin_setting, '__iter__'):
            for item in admin_setting:
                self.register(item, setting_cache=setting_cache)

        else:

            if admin_setting.key() in self._registry.keys():
                raise AlreadyRegistered('The setting %s has already been '
                    'registered' % admin_setting.__name__)

            try:
                model_object = setting_cache.get(name=admin_setting.name)
                value = SettingValue(model_object.value.value)
                value.model_object = model_object
            except AdminSetting.DoesNotExist:
                value = SettingValue(admin_setting.default)
                value.model_object = None
            value.setting_object = admin_setting

            self._registry[admin_setting.key()] = value


    def unregister(self, admin_setting):
        """
        Unregisters a given setting. If it has not been registered, this will
        raise NotRegistered.
        """
        if admin_setting.key() not in self._registry.keys:
            raise NotRegistered('The setting %s cannot be unregistered as it '
                'has not been registered' % admin_setting.__name__)
        del self._registry[admin_setting.key()]


settings = cache.get(CACHE_NAME)
if not settings:
    cache.set(CACHE_NAME, AdminSettingSite(), CACHE_TTL)
    settings = cache.get(CACHE_NAME)