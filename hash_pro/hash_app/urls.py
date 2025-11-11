from django.urls import path
from . import views
urlpatterns=[
    path("welcome/",view=views.welcome),
    path('register/',view=views.register),
    path('login/',view=views.login)
]