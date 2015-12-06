from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/$', views.index, name='event_index'),
    url(r'^events/(?P<event_id>[0-9]+)/$', views.show, name='event_detail'),
    url(r'^events/(?P<event_id>[0-9]+)/register/$', views.register, name='event_register'),

    url(r'^user/info/(?P<type>[pc])/$', views.myinfo, name='myinfo'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
]
