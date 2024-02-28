from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from server.models import RootPageSettings
from xmppserverui.mixins import PageContextMixin, ServerInstalledMixin
from django.conf import settings
from .config import WHITENOISE_ROOT
from .forms import XabberWebConfigForm
from .models import XabberWebSettings
from .config import domains_to_string, get_xabber_config, update_config, XABBER_WEB_VER


class RootView(ServerInstalledMixin, TemplateView):
    template_name = 'xabber_web/index.html'

    def get(self, request, *args, **kwargs):
        xabber_web_config = get_xabber_config()
        for key, value in xabber_web_config.items():
            if isinstance(value, str) and value not in ('true', 'false'):
                xabber_web_config[key] = "'{}'".format(value)

        context = {'config': xabber_web_config}
        if XABBER_WEB_VER:
            context['xabber_web_ver'] = XABBER_WEB_VER
        return self.render_to_response(context=context)


class XabberWebInfoView(PageContextMixin, TemplateView):
    template_name = 'xabber_web/info.html'

    def get(self, request, *args, **kwargs):
        current_root_page = str(RootPageSettings.objects.all().first())
        warning = None
        if current_root_page not in __package__:
            warning = 'Set "Xabber for Web" as the root page in the settings'
        current_config = domains_to_string(get_xabber_config())
        form = XabberWebConfigForm(initial=current_config)
        return self.render_to_response(context={'warning': warning, 'form': form})

    def post(self, request, *args, **kwargs):
        if request.POST.get('reset'):
            XabberWebSettings.objects.all().delete()
            return HttpResponseRedirect(reverse('xabber_web:info'))
        else:
            form = XabberWebConfigForm(request.POST)
            if form.is_valid():
                update_config(form.cleaned_data)
                return HttpResponseRedirect(reverse('xabber_web:info'))
            return self.render_to_response(context={'form': form})
