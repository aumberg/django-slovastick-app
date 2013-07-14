from django.conf.urls import patterns, url

urlpatterns = patterns('slovastick_app.views',
    url(r'^(?P<text>\S+)$', 'index'),
    url(r'^$', 'hello'),
)