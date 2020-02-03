from django.urls import path
from . import views

urlpatterns = [
    # DJANGO URL PATTERNS: An Introduction
    # The URLs you will place here will allow you to bind specific "views"
    # to your URLs. The views referenced here are defined in the views.py
    # file. Whatever you do, those views should either return an HttpResponse
    # or a JsonResponse in order to function normally.

    # CREATING A URL PATTERN
    #
    # path(r'<your_desired_url>', views.your_view_def, name='your_view_name')
    # EXAMPLE: path(r'functions/save', views.save, name='save')
    #
    # WHERE:
    # your_desired_url => any combination of URL string; it is recommended to
    # keep this as short as possible and only add URL params if needed.
    # NOTE: THERE IS NO NEED TO INCLUDE A FULL URL HERE; DOING SO WILL CAUSE
    # YOUR URL PATTERN TO FAIL.
    #
    # your_view_def => the definition name to use as defined in the views.py file.
    # The framework will use the view defined as the URL's template. If you have
    # a def login(request) function, then you put it as views.login.
    #
    # your_view_name => the string to use as reference for the URL pattern. Only
    # used for non-API Django usage. Preferrably to be kept the same name as the view.

    # path(r'ionic/testcomm', views.testComms, name='testComms'),
    path(r'ionic/stargazer', views.stargazer, name='stargazer'),
    path(r'ionic/lovelive', views.stars, name='stars'),
]
