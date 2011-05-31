from copy import copy
from functools import update_wrapper

from django.contrib.admin.sites import AdminSite
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache

from adminsettings.conf import settings


class SettingsAdminSite(AdminSite):

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = patterns('',
            url(r'^settings/$',
                wrap(self.settings),
                name='settings'),
        )
        return urlpatterns

    @never_cache
    def settings(self, request):
        admin_settings = []
        for setting in settings._obj_registry:
            value = settings._registry[setting.key()]
            admin_settings.append(setting(value))
        return TemplateResponse(request, ['adminsettings/index.html'], {
            'title': 'Settings',
            'admin_settings': sorted(admin_settings, key=lambda s: s.weight),
        })

adminsettings_site = SettingsAdminSite('adminsettings')