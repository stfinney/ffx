from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/$', views.index, name='event_index'),
    url(r'^events/(?P<event_id>[0-9]+)/$', views.show, name='event_detail'),

]
