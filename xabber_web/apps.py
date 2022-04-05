import os
from django.apps import AppConfig


class ModuleConfig(AppConfig):
    name = 'modules.xabber_web'
    verbose_name = 'Xabber Web'
    root_page = True
    whitenoise_root_path = os.path.join('modules', 'xabber_web', 'static', 'xabberweb')
