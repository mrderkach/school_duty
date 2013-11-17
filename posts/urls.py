from django.conf.urls import patterns, url
from posts import views

urlpatterns = patterns('',
    url(r'^$', views.detail, name='details')
)