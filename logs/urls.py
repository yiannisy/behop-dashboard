from django.conf.urls import patterns, url

from logs import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^clients', views.ClientsListView.as_view(), name='clients')
)
