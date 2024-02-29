import os
from modules.xabber_web.models import XabberWebSettings
from xabber_server_panel.base_modules.registration.models import RegistrationSettings
from xabber_server_panel.base_modules.config.models import VirtualHost

IS_ROOT_PAGE = True
DOMAIN_LISTS = ('LOGIN_DOMAINS', 'REGISTRATION_DOMAINS', 'TRUSTED_DOMAINS')


def domains_to_list(config_dict, is_form=False):
    for key in DOMAIN_LISTS:
        value = config_dict.get(key, False)
        if value and isinstance(value, str):
            if is_form:
                config_dict[key] = [_str.strip() for _str in value.splitlines()]
            else:
                config_dict[key] = value.split(',')
    return config_dict


def domains_to_string(config_dict):
    for key in DOMAIN_LISTS:
        value = config_dict.get(key, False)
        if value:
            config_dict[key] = '\n'.join(value)
    return config_dict


def get_xabber_config():
    return _get_xabber_config()


def init_form():
    return domains_to_string(_get_xabber_config(is_init_form=True))


def _get_xabber_config(is_init_form=False):
    """
    debug, trusted_domains, check_version - immutable
    """
    vhosts = list(VirtualHost.objects.order_by('name').values_list('name', flat=True))
    reg_vhosts = list(RegistrationSettings.objects.order_by('host__name').values_list('host__name', flat=True))
    template_config = {
        "CONNECTION_URL": None,
        "DISABLE_LOOKUP_WS": "true",
        "LOG_LEVEL": "ERROR",
        "MAIN_COLOR": "red",
        "LOGIN_DOMAINS": vhosts,
        "REGISTRATION_DOMAINS": reg_vhosts if reg_vhosts else None,
        "TRUSTED_DOMAINS": vhosts,
        "RECOMMENDED_DOMAIN": None,
        "TURN_SERVERS_LIST": None,
        "CHECK_VERSION": "false",
        "REGISTRATION_CUSTOM_DOMAIN": "false",
        "LOGIN_CUSTOM_DOMAIN": "false",
        "REGISTRATION_BUTTON": "true",
        "ASSETS_URL_PREFIX": "static/xabberweb/"
    }
    xabberweb_settings = XabberWebSettings.objects.all()
    if xabberweb_settings:
        enable_advanced = False

        for obj in xabberweb_settings.values():
            if obj.get('key') not in ["LOGIN_DOMAINS", "REGISTRATION_DOMAINS", "REGISTRATION_BUTTON"]:
                enable_advanced = True
            template_config[obj.get('key')] = obj.get('value')
        if is_init_form and enable_advanced:
            template_config['is_enabled'] = True
    return domains_to_list(template_config)


def update_config(form):
    current_config = get_xabber_config()
    for key, value in form.items():
        if key in current_config and form[key] != current_config[key]:
            value = ','.join(value) if isinstance(value, list) else value
            if value is None:
                try:
                    XabberWebSettings.objects.get(key=key).delete()
                except:
                    pass
            else:
                try:
                    config_key = XabberWebSettings.objects.get(key=key)
                    config_key.value = value
                    config_key.save()
                except XabberWebSettings.DoesNotExist:
                    XabberWebSettings.objects.create(key=key, value=value)


# automatically overwritten when making a build
XABBER_WEB_VER = None
