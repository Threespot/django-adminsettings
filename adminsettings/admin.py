from __future__ import with_statement
from copy import copy
from functools import update_wrapper

from django.contrib.admin.sites import AdminSite
from django.db import transaction
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache

from adminsettings.conf import settings
from adminsettings.models import AdminSetting


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

        if request.method == 'POST':
            with transaction.commit_on_success():
                for key, value in settings._registry.iteritems():
                    pass

        admin_settings = [s[1] for s in sorted(settings._registry.iteritems(), \
            key=lambda s: s[1].setting_object.weight)]
        return TemplateResponse(request, ['adminsettings/index.html'], {
            'title': 'Settings',
            'admin_settings': admin_settings,
        })

adminsettings_site = SettingsAdminSite('adminsettings')