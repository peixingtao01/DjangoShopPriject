from django.urls import path
from ShopFresh1.views import *

urlpatterns =[
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('404/',page404),
]