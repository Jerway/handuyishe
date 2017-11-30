from django.conf.urls import url
from App import views

urlpatterns = [

    url(r'^index/', views.index, name='index'),
    url(r'^classify/(.*?)/', views.classify, name='classify'),
    url(r'^page_chage/(.*?)/(.*?)/(.*?)/', views.page_chage, name='page_chage'),
    url(r'^register/', views.register, name='register'),


]











