from django.apps import AppConfig


class ModuleConfig(AppConfig):
    name = 'modules.xabber_web'
    verbose_name = 'Xabber Web'
    EXCLUDED_PERMISSIONS_MODELS = ['xabberwebsettings']
