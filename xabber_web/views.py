from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from xabber_server_panel.base_modules.config.models import RootPage
from xabber_server_panel.base_modules.users.decorators import permission_read, permission_write
from .forms import XabberWebConfigForm
from .models import XabberWebSettings
from .config import get_xabber_config, update_config, XABBER_WEB_VER, init_form


class RootView(TemplateView):
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


class XabberWebInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'xabber_web/info.html'
    app = 'xabber_web'

    @permission_read
    def get(self, request, *args, **kwargs):
        current_root_page = str(RootPage.objects.all().first())
        warning = None
        if current_root_page not in __package__:
            warning = 'Set "Xabber for Web" as the root page in the settings'
        current_config = init_form()
        print(current_config)
        form = XabberWebConfigForm(initial=current_config)
        return self.render_to_response(context={'warning': warning, 'form': form})

    @permission_write
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
