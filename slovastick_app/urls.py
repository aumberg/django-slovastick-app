from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings

urlpatterns = patterns('',
    # url(r'^$', 'sound.views.test'),s
    url(r'^$','slovastick_app.views.hello'),
    url(r'^', 'slovastick_app.views.index')
)