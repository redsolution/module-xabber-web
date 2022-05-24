from django import forms
from .config import domains_to_list


class XabberWebConfigForm(forms.Form):

    BOOL_CHOICE = (
        ('true', 'true'),
        ('false', 'false')
    )
    COLORS = (('red', 'red'), ('pink', 'pink'), ('purple', 'purple'), ('deep-purple', 'deep-purple'),
              ('indigo', 'indigo'), ('blue', 'blue'), ('light-blue', 'light-blue'), ('cyan', 'cyan'),
              ('teal', 'teal'), ('green', 'green'), ('light-green', 'light-green'), ('lime', 'lime'),
              ('amber', 'amber'), ('orange', 'orange'), ('deep-orange', 'deep-orange'),
              ('brown', 'brown'), ('blue-grey', 'blue-grey'))

    LOG_LEVEL_CHOICE = (
        ('NONE', 'NONE'),
        ('ERROR', 'ERROR'),
        ('WARN', 'WARN'),
        ('INFO', 'INFO'),
        ('DEBUG', 'DEBUG')
    )

    CONNECTION_URL = forms.CharField(
        max_length=200,
        required=False,
        empty_value=None,
        label='Connection url',
        widget=forms.TextInput(attrs={
            'size': 40,
            'hint': 'WebSocket URL used for creating connections'
        })
    )
    DISABLE_LOOKUP_WS = forms.ChoiceField(
        required=False,
        label='Disable lookup web socket url',
        initial='true',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': 'Disable lookup for domain using websocket known hosts'
        })
    )

    LOG_LEVEL = forms.ChoiceField(
        required=False,
        label='Log level',
        choices=LOG_LEVEL_CHOICE,
        widget=forms.Select(attrs={
            'hint': 'Strophe console log level'
        })
    )

    LOGIN_DOMAINS = forms.CharField(
        required=False,
        label='Login domains',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'hint': 'Domains list used for account authentication'
        })
    )

    REGISTRATION_DOMAINS = forms.CharField(
        required=False,
        label='Registration domains',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'hint': 'Domains list used for account registration'
        })
    )

    RECOMMENDED_DOMAIN = forms.CharField(
        required=False,
        empty_value=None,
        label='Recommended domain',
        widget=forms.TextInput(attrs={
            'size': 40,
            'hint': 'Domain recommended for account registration when authentication occurs on a server where not all '
                    'client functions are supported. '
        })
    )

    TURN_SERVERS_LIST = forms.CharField(
        max_length=100,
        required=False,
        empty_value=None,
        label='Turn servers list',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'hint': 'Servers for Jingle Message connection'
        })
    )

    REGISTRATION_CUSTOM_DOMAIN = forms.ChoiceField(
        required=False,
        label='Registration on custom domain',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': 'Decides whether registration on domains not listed in REGISTRATION_DOMAINS is possible'
        })
    )

    REGISTRATION_BUTTON = forms.ChoiceField(
        required=False,
        label='Show registration button',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': 'Show/Hide registration button'
        })
    )

    LOGIN_CUSTOM_DOMAIN = forms.ChoiceField(
        required=False,
        label='Login to custom domains',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': 'Decides whether authentication on domains not listed in LOGIN_DOMAINS is possible'
        })
    )

    MAIN_COLOR = forms.ChoiceField(
        required=False,
        label='Main color',
        choices=COLORS,
        widget=forms.Select(attrs={
            'hint': 'Main client color for elements'
        })
    )

    is_enabled = forms.BooleanField(
        required=False,
        label='Advanced settings',
        initial=False
    )

    def clean(self, *args, **kwargs):
        cleaned_data = domains_to_list(self.cleaned_data, is_form=True)
        del cleaned_data['is_enabled']
        return cleaned_data
