from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'test', views.testView, name='testView'),
    path(r'analyze/mode=lexicon', views.analyzeLexiconMatching, name='analyzeLexiconMatching'),
    path(r'analyze/mode=classifier', views.analyzeClassifier, name='analyzeClassifier'),
    path(r'create', views.createTable, name='createTable'),
    path(r'write', views.writeToTable, name='writeToTable')
]
