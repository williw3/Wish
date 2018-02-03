from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^show/(?P<id>\d+)$', views.show),
	url(r'^add/(?P<id>\d+)$', views.add),
	url(r'^delete/(?P<id>\d+)$', views.delete),
	url(r'^landing$', views.landing),
	url(r'^new$', views.new),
	url(r'^create$', views.create),
	url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]