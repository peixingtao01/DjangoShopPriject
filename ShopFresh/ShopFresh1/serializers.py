#规定接口模型和数据字段
from rest_framework import serializers
from ShopFresh1.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #声明数据是谁
    class Meta:#元类
        model = Goods
        fields = ['goods_name','goods_price','goods_number','goods_description','id','goods_date','goods_safeDate']

class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    #声明要查询是什么表
    class Meta:
        model = GoodsType
        fields = ['name','description']
