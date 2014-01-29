from django.conf.urls import patterns, url
from logs import views

urlpatterns = patterns(
    '',
    url(r'^stats',views.show_stats,name='stats'),
    url(r'^usage',views.total_usage,name='usage'),
    url(r'^report',views.report,name='report'),
)
