from django.urls import path,re_path
from Buyer.views import *

urlpatterns =[
    path('register/',register),
    path('login/',login),
    path('index/',index),
]
urlpatterns+=[
    path('logout/',logout),
]

urlpatterns+=[
    path('goods_list/',goods_list),
    path('goods_detail/',goods_detail)
]