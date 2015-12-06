from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/$', views.index, name='event_index'),
    url(r'^events/(?P<event_id>[0-9]+)/$', views.show, name='event_detail'),
    url(r'^events/(?P<event_id>[0-9]+)/register/$', views.register, name='event_register'),

    url(r'^myinfo_p/', views.myinfo_p, name='myinfo_p'),
    url(r'^myinfo_c/', views.myinfo_c, name='myinfo_c'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^reg/', views.reg, name='register'),
]
