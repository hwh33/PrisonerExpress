from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SE_Project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',include('PrisonerExpress.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fun/',include('PrisonerExpress.urls')),
)
