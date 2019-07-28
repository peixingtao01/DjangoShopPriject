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
    path('^goods_list/',goods_list),
    # re_path(r'goods_detail/(?P<goods_id>\d+)',goods_detail),
    path('goods_detail/',goods_detail),
    path('pay_order/',pay_order),
]

urlpatterns+=[
    path('cart_add/',cart_add),#加入购物车
    path('cart/',cart),#购物车
]