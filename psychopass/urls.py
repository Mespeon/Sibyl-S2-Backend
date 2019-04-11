from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'test', views.testView, name='testView'),
    path(r'analyze', views.analyzeThis, name='analyzeThis'),
]
