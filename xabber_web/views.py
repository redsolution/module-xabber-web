from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from server.models import RootPageSettings
from xmppserverui.mixins import PageContextMixin
from django.conf import settings
from .config import WHITENOISE_ROOT
from .forms import XabberWebConfigForm
from .models import XabberWebSettings
from .utils import get_config, update_config


class RootView(PageContextMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        xabber_web_config = get_config()
        xabber_web_config['LOGIN_DOMAINS'] = xabber_web_config['LOGIN_DOMAINS'].split(',')
        xabber_web_config['REGISTRATION_DOMAINS'] = xabber_web_config['REGISTRATION_DOMAINS'].split(',')
        xabber_web_config = {key: value for key, value in xabber_web_config.items() if value is not None}
        return self.render_to_response(context={'config': xabber_web_config})


class XabberWebInfoView(PageContextMixin, TemplateView):
    template_name = 'info.html'

    def get(self, request, *args, **kwargs):
        current_root_page = str(RootPageSettings.objects.all().first())
        warning = None
        if current_root_page not in __package__:
            warning = 'Set "Xabber for Web" as the root page in the settings and restart server'
        else:
            try:
                wn_root = settings.WHITENOISE_ROOT
                if WHITENOISE_ROOT != wn_root:
                    warning = 'The server restart is required'
            except Exception:
                warning = 'Server restart required'
        current_config = get_config()
        current_config['LOGIN_DOMAINS'] = current_config['LOGIN_DOMAINS'].replace(',', '\n')
        current_config['REGISTRATION_DOMAINS'] = current_config['REGISTRATION_DOMAINS'].replace(',', '\n')
        form = XabberWebConfigForm(initial=current_config)
        return self.render_to_response(context={'warning': warning, "form": form})

    def post(self, request, *args, **kwargs):
        if request.POST.get('reset'):
            XabberWebSettings.objects.all().delete()
            return HttpResponseRedirect(reverse('xabber_web:info'))
        else:
            form = XabberWebConfigForm(request.POST)
            if form.is_valid():
                update_config(form.cleaned_data)
                return HttpResponseRedirect(reverse('xabber_web:info'))
            return self.render_to_response(context={"form": form})
