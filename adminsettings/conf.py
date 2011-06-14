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

    def register(self, SettingClass, setting_cache=None):
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
        if hasattr(SettingClass, '__iter__'):
            for item in SettingClass:
                self.register(item, setting_cache=setting_cache)

        else:

            if SettingClass.key() in self._registry.keys():
                raise AlreadyRegistered('The setting %s has already been '
                    'registered' % SettingClass.__name__)

            try:
                model_object = setting_cache.get(name=SettingClass.key())
            except AdminSetting.DoesNotExist:
                setting_value = SettingValue(SettingClass.default)
                setting_value.model_object = None
                setting_value.setting_object = SettingClass(SettingClass.default)
            else:
                setting_value = SettingValue(model_object.value)
                setting_value.model_object = model_object
                setting_value.setting_object = SettingClass(model_object.value)
            finally:
                self._registry[SettingClass.key()] = setting_value


    def unregister(self, SettingClass):
        """
        Unregisters a given setting. If it has not been registered, this will
        raise NotRegistered.
        """
        if SettingClass.key() not in self._registry.keys:
            raise NotRegistered('The setting %s cannot be unregistered as it '
                'has not been registered' % SettingClass.__name__)
        del self._registry[SettingClass.key()]


settings = cache.get(CACHE_NAME)
if not settings:
    cache.set(CACHE_NAME, AdminSettingSite(), CACHE_TTL)
    settings = cache.get(CACHE_NAME)