from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'register', views.register, name='register'),
    path(r'login', views.login, name='login'),
    path(r'reg_form', views.register_form, name='register_form'),
    path(r'success', views.regSuccess, name='regSuccess')
]
