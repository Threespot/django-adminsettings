def autodiscover():
    """
    Auto-discover registered subclasses of PageLayout living in models.py files
    in any application in settings.INSTALLED_APPS by attempting to import and
    failing silently if need be.
    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    from adminsettings.conf import settings as adminsettings

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            before_import_registry = copy.copy(adminsettings._registry)
            import_module('%s.settings' % app)
        except:
            adminsettings._registry = before_import_registry
            if module_has_submodule(mod, 'settings'):
                raise