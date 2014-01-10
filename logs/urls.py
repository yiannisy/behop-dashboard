from django.conf.urls import patterns, url
from logs import views

urlpatterns = patterns(
    '',
    url(r'^stats',views.show_stats,name='stats')
)
