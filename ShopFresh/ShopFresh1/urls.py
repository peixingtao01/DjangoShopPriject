from django.urls import path,re_path
from ShopFresh1.views import *

urlpatterns =[
    path('register/',register),
    path('login/',login),
    # re_path(r'^$/',login),
    path('index/',index),
    path('logout/',logout),
    re_path('^$',index),#首页得这么写
    # path('404/',page404),
    # path('buttons/',buttons),
    # path('cards/',cards),
    # path('charts/',charts),
    # path('table/',tables),
    # path('utilltiesanimation/',utilltiesanimation),

]
urlpatterns+=[
    path('register_store/',register_store),
    path('add_goods/',add_goods),
    re_path(r'list_goods/(?P<state>\w+)',list_goods),
    re_path(r'^goods_detail/(?P<goods_id>\d+)',goods_detail),
    re_path(r'goods_update/(?P<goods_id>\d+)',goods_update),
]

urlpatterns+=[
    path('under_goods/',under_goods),
    re_path(r'set_goods/(?P<state>\w+)',set_goods),
]

