from django.conf.urls import url, include
from .views import RootView, XabberWebInfoView

app_name = 'xabber_web'

urlpatterns = [
    url(r'^info', XabberWebInfoView.as_view(), name='info'),
    url(r'^$', RootView.as_view(), name='root'),
]
