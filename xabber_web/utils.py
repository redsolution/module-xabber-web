from modules.xabber_web.models import XabberWebSettings
from registration.models import RegistrationSettings
from virtualhost.models import VirtualHost


def get_config():
    """
    debug, trusted_domains, check_version - immutable
    """
    template_config = {
        "CONNECTION_URL": "(window.location.protocol === 'https:' ? 'wss' : 'ws') + '://' + window.location.hostname  + (window.location.protocol === 'https:' ? ':5443/wss' : ':5280/ws')",
        "DISABLE_LOOKUP_WS": "true",
        "LOG_LEVEL": "ERROR",
        "MAIN_COLOR": "red",
        "DEBUG": "true",
        "LOGIN_DOMAINS": ','.join([obj.name for obj in VirtualHost.objects.all()]),
        "REGISTRATION_DOMAINS": ','.join(sorted([obj.vhost.name for obj in RegistrationSettings.objects.all()])),
        "TRUSTED_DOMAINS": None,
        "RECOMMENDED_DOMAIN": None,
        "TURN_SERVERS_LIST": None,
        "CHECK_VERSION": "false",
        "REGISTRATION_CUSTOM_DOMAIN": "false",
        "LOGIN_CUSTOM_DOMAIN": "false",
    }
    xabberweb_settings = XabberWebSettings.objects.all()
    if xabberweb_settings:
        for obj in xabberweb_settings.values():
            template_config[obj.get('key')] = obj.get('value')
    return template_config


def update_config(form):
    current_config = get_config()
    form['LOGIN_DOMAINS'] = ','.join(form['LOGIN_DOMAINS'].splitlines())
    form['REGISTRATION_DOMAINS'] = ','.join(form['REGISTRATION_DOMAINS'].splitlines())

    for key, value in form.items():
        if key in current_config and set(str(form[key])) != set(str(current_config[key])):
            try:
                config_key = XabberWebSettings.objects.get(key=key)
                config_key.value = value
                config_key.save()
            except XabberWebSettings.DoesNotExist:
                XabberWebSettings.objects.create(key=key, value=value)

