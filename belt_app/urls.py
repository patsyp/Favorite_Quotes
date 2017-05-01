from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.createUser),
	url(r'^login$', views.login),
	url(r'^quotes$', views.success),
	url(r'^logout$', views.logout),
	url(r'^add_quote$', views.createQuote),
	url(r'^quotes/favorite/(?P<id>\d+)$', views.favorite),
	url(r'^quotes/remove/(?P<id>\d+)$', views.remove),
	url(r'^quotes/users/(?P<id>\d+)$', views.showUser),
	]