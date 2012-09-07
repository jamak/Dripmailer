from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'drips.views.home', name='home'),
    # url(r'^drips/', include('drips.foo.urls')),

    url(r'^campaigns/$', 'drip_emailer.views.campaign_index'),
    url(r'^campaigns/(?P<campaign_id>\d+)/$', 'drip_emailer.views.campaign_detail'),
    url(r'^emails/$', 'drip_emailer.views.email_index'),
    url(r'^emails/(?P<email_id>\d+)/$', 'drip_emailer.views.email_detail'),
    url(r'^prospects/$', 'drip_emailer.views.prospect_index'),
    url(r'^prospects/(?P<prospect_id>\d+)/$', 'drip_emailer.views.prospect_detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),


)
