from django.contrib.contenttypes.generic import GenericStackedInline
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

from adminsettings.exceptions import AlreadyRegistered, NotRegistered
from adminsettings.models import AdminSetting

CACHE_NAME = 'adminsettings_cache'
CACHE_TTL = 10


class AdminSettingSite(object):

    def __init__(self):
        self._obj_registry = []
        self._registry = {}

    def __iter__(self):
        return self._registry.__iter__()

    def register(self, admin_setting, setting_cache=None):
        """
        Registers a given setting. If it has already been registered, this
        will raise AlreadyRegistered.

        The configuration values are stored in the database, as instances of the
        class that defines them. So, here:
        admin_setting = the setting class
        db_obj        = the stored instance the Django model
        db_obj.value  = the stored instance of the setting class
        """

        # To prevent multiple DB lookups, let's run and evaluate the queryset,
        # which allows us to pass on the value to any sub-registrations (i.e. if
        # a list was passed to the function)
        if not setting_cache:
            setting_cache = AdminSetting.objects.all()

        if hasattr(admin_setting, '__iter__'):
            for item in admin_setting:
                self.register(item, setting_cache=setting_cache)
        else:
            if admin_setting in self._obj_registry:
                raise AlreadyRegistered('The setting %s has already been '
                    'registered' % admin_setting.__name__)
            self._obj_registry.append(admin_setting)
            setting_name = admin_setting.key()
            try:
                db_obj = setting_cache.get(name=admin_setting.name)
                self._registry[setting_name] = db_obj.value.value
            except AdminSetting.DoesNotExist:
                self._registry[setting_name] = admin_setting.default

    def unregister(self, admin_setting):
        """
        Unregisters a given setting. If it has not been registered, this will
        raise NotRegistered.
        """
        if admin_setting not in self._obj_registry:
            raise NotRegistered('The setting %s cannot be unregistered as it '
                'has not been registered' % admin_setting.__name__)
        self._obj_registry.remove(admin_setting)


settings = cache.get(CACHE_NAME)
if not settings:
    cache.set(CACHE_NAME, AdminSettingSite(), CACHE_TTL)
    settings = cache.get(CACHE_NAME)