from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/', views.index, name='index'),
    url(r'^a/', views.myinfo, name='myinfo'),
    url(r'^signin/', views.signin, name='signin'),
]
