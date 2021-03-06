"""ShopFresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path,include,re_path
from Buyer.views import index

# -------------------------------------------------------API

# from rest_framework import routers,serializers,viewsets
from rest_framework import routers

from ShopFresh1.views import UserViewSet,TypeViewSet
router = routers.DefaultRouter()#声明一个默认的路由注册器
router.register(r'goods',UserViewSet)
router.register(r'goodsType',TypeViewSet)


# -------------------------------------------------------API
urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/',include('ShopFresh1.urls')),
    path('buyer/',include('Buyer.urls')),
    path('ckeditor',include('ckeditor_uploader.urls')),
]
urlpatterns+=[
    re_path(r'^$',index),
]

urlpatterns+=[
    re_path('^API',include(router.urls)),#@声明一个默认的路由注册器
    # re_path('^api-auth',include('rest-framework.urls')),
]