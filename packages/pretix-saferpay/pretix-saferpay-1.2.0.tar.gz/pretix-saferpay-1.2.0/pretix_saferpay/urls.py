from django.conf.urls import include, url

from pretix.multidomain import event_url
from .views import (
    ReturnView, WebhookView, redirect_view,
)

event_patterns = [
    url(r'^saferpay/', include([
        event_url(r'^webhook/(?P<payment>[0-9]+)/$', WebhookView.as_view(), name='webhook', require_live=False),
        url(r'^redirect/$', redirect_view, name='redirect'),
        url(r'^return/(?P<order>[^/]+)/(?P<hash>[^/]+)/(?P<payment>[0-9]+)/(?P<action>[^/]+)$', ReturnView.as_view(),
            name='return'),
    ])),
]
