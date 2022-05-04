from django import forms


class XabberWebConfigForm(forms.Form):

    BOOL_CHOICE = (
        ('true', 'true'),
        ('false', 'false')
    )

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
        label='Connection url',
        widget=forms.TextInput(attrs={
            'size': 40,
            'hint': "WebSocket URL used for creating connections"
        })
    )
    DISABLE_LOOKUP_WS = forms.ChoiceField(
        required=False,
        label='Disable lookup web socket url',
        initial='true',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': "Disable lookup for domain using websocket known hosts"
        })
    )

    LOG_LEVEL = forms.ChoiceField(
        required=False,
        label='Log level',
        choices=LOG_LEVEL_CHOICE,
        widget=forms.Select(attrs={
            'hint': "Strophe console log level"
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
        label='Recommended domain',
        widget=forms.TextInput(attrs={
            'size': 40,
            'hint': "Domain recommended for account registration when authentication occurs on a server where not all "
                    "client functions are supported. "
        })
    )

    TURN_SERVERS_LIST = forms.CharField(
        max_length=100,
        required=False,
        label='Turn servers list',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'hint': "Servers for Jingle Message connection"
        })
    )

    REGISTRATION_CUSTOM_DOMAIN = forms.ChoiceField(
        required=False,
        label='Registration on custom domain',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': "Decides whether registration on domains not listed in REGISTRATION_DOMAINS is possible"
        })
    )

    LOGIN_CUSTOM_DOMAIN = forms.ChoiceField(
        required=False,
        label='Login to custom domains',
        choices=BOOL_CHOICE,
        widget=forms.Select(attrs={
            'hint': "Decides whether authentication on domains not listed in LOGIN_DOMAINS is possible"
        })
    )

    MAIN_COLOR = forms.CharField(
        required=False,
        label='Main color',
        widget=forms.TextInput(attrs={
            'hint': "Main client color for elements"
        })
    )

    is_enabled = forms.BooleanField(
        required=False,
        label='Advanced settings',
        initial=False
    )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        del cleaned_data['is_enabled']

