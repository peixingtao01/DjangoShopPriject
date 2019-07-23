from django.urls import path,re_path
from ShopFresh1.views import *

urlpatterns =[
    path('register/',register),
    path('login/',login),
    path('index/',index),
    re_path('^$',index),#首页得这么写
    path('404/',page404),
    path('buttons/',buttons),
    path('cards/',cards),
    path('charts/',charts),
    path('table/',tables),
    path('utilltiesanimation/',utilltiesanimation),

]
urlpatterns+=[
    path('register_store/',register_store),
    path('add_goods/',add_goods),
    path('list_goods/',list_goods),
]