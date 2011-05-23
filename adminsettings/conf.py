from django.contrib.contenttypes.generic import GenericStackedInline
from django.core.exceptions import ImproperlyConfigured

from adminsettings.exceptions import AlreadyRegistered, NotRegistered


class AdminSettingSite(object):

    def __init__(self):
        self._registry = []

    def __iter__(self):
        return self._registry.__iter__()

    def register(self, admin_setting):
        """
        Registers a given setting. If it has already been registered, this
        will raise AlreadyRegistered.
        """
        if hasattr(admin_setting, '__iter__'):
            for item in admin_setting:
                self.register(item)
        else:
            if admin_setting in self._registry:
                raise AlreadyRegistered('The setting %s has already been '
                    'registered' % admin_setting.__name__)
            self._registry.append(admin_setting)

    def unregister(self, admin_setting):
        """
        Unregisters a given setting. If it has not been registered, this will
        raise NotRegistered.
        """
        if admin_setting not in self._registry:
            raise NotRegistered('The setting %s cannot be unregistered as it '
                'has not been registered' % admin_setting.__name__)
        self._registry.remove(admin_setting)


settings = AdminSettingSite()