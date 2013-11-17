from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', 'posts.views.prelog', name='prelog'),
    url(r'^logcheck/', 'posts.views.login_view', name='checklog'),
    url(r'^logout/', 'posts.views.logout_view', name='logout'),
    url(r'^regcheck/', 'posts.views.registration_view', name='checkreg'),
    url(r'^registration/', 'posts.views.prereg', name='prereg'),
    url(r'^$', 'posts.views.home', name='home'),
    url(r'^posts/(?P<post_id>\d+)/', include('posts.urls', namespace="posts")),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
