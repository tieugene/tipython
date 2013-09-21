from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reception/', include('reception.urls', namespace='reception')),
    url(r'^clients/', include('clients.urls', namespace='clients')),


)

