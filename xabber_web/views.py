from django.views.generic import TemplateView
from server.models import RootPageSettings
from xmppserverui.mixins import AuthMixin
from django.conf import settings
from .apps import ModuleConfig


class RootView(TemplateView):
    template_name = 'index.html'


class XabberWebInfoView(AuthMixin, TemplateView):
    template_name = 'info.html'

    def get(self, request, *args, **kwargs):
        current_root_page = str(RootPageSettings.objects.all().first())
        self_name = __package__
        warning = None
        if current_root_page not in self_name:
            warning = 'Set "Xabber for Web" as the root page in the settings and restart server'
        else:
            try:
                wn_root = settings.WHITENOISE_ROOT
                if ModuleConfig.whitenoise_root_path != wn_root:
                    warning = 'The server restart is required'
            except:
                warning = 'Server restart required'

        return self.render_to_response(context={'warning': warning})
