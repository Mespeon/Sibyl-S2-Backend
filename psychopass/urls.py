from django.urls import path
from . import views

urlpatterns = [
    #path(r'', views.index, name='index'),
    #path(r'test', views.testView, name='testView'),
    path(r'analyze/mode=lexicon', views.analyzeLexiconMatching, name='analyzeLexiconMatching'),
    path(r'analyze/mode=classifier', views.analyzeClassifier, name='analyzeClassifier'),
    path(r'create', views.createTable, name='createTable'),
    path(r'write', views.writeToTable, name='writeToTable'),
    path(r'prepare', views.prepareData, name='prepareData'),
    path(r'statistics', views.prepareStatistics, name='prepareStatistics'),
    path(r'classify', views.aggregatedClassify, name='aggregatedClassify'),
    path(r'thanks', views.thanks, name='thanks'),

    #Ionic App API Test Functions
    path(r'ionic/testcomm', views.testComms, name='testComms'),
    path(r'ionic/stargazer', views.stargazer, name='stargazer'),
    path(r'ionic/lovelive', views.stars, name='stars'),

    #For Vivien
    path(r'vivien/hello', views.forVivien, name='forVivien'),
    path(r'vivien/senpai', views.forSenpai, name='forSenpai'),

    #For COE Toothbrush
    path(r'coe/like', views.coeLike, name='coeLike'),
    path(r'coe/react', views.coeReact, name='coeReact'),
]
