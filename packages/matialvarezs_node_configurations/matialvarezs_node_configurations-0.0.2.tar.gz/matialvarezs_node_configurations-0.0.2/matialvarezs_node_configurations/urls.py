from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION >= (2, 0):
	from django.urls import include, path, re_path as url
else:
	from django.conf.urls import include, url

from . import views

app_name = "matialvarezs_node_configurations"

urlpatterns = [
	url('', views.index, name='index'),
	url(r'api/', include('matialvarezs_node_configurations.api.urls', namespace='api')),
]


