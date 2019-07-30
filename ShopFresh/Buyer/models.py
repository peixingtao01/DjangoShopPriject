# Create your models here.
from django.db import models
from ShopFresh1.models import Store,Goods
# Create your models here.

class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    email = models.EmailField(verbose_name='用户邮箱')
    phone = models.CharField(max_length=32,verbose_name='联系电话',blank=True,null=True)
    connect_address = models.TextField(verbose_name='联系地址',blank=True,null=True)

class Address(models.Model):
    address = models.TextField(verbose_name='收货地址',blank=True,null=True)
    recver = models.CharField(max_length=32,verbose_name='收件人',blank=True,null=True)
    recver_num = models.CharField(max_length=32,verbose_name='收件人电话',blank=True,null=True)
    post_num = models.CharField(max_length=32,verbose_name='邮编',blank=True,null=True)
    buyer_id = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name='用户id')
    # 数据库名小写加下划线id
# class GoodsImg(models.Model):
#     img_address = models.ImageField(upload_to='store/images',verbose_name='图片地址')
#     img_description = models.TextField(verbose_name='图片描述')
#     goods_id = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name='商品id')
#
# class GoodsType(models.Model):
#     name = models.CharField(max_length=32,verbose_name='商品类型名称')
#     description = models.TextField(max_length=32,verbose_name='商品类型描述')
#     picture = models.ImageField(upload_to='buyer/images')
class Cart(models.Model):
    # user_id = models.IntegerField(verbose_name='买家id',blank=True,null=True)
    goods_id = models.IntegerField(verbose_name='货物id',blank=True,null=True)
    goods_number = models.IntegerField(verbose_name='货物数量',default=1)
    goods_name = models.CharField(max_length=32, verbose_name='商品名称',blank=True,null=True)
    goods_price = models.FloatField(verbose_name='商品价格',blank=True,null=True)
    goods_image = models.ImageField(upload_to='shopfresh1/images', verbose_name='商品图片',blank=True,null=True)
    goods_total = models.FloatField(verbose_name='总价')
    goods_under = models.IntegerField(verbose_name='商品状态', default=1)
    goods_addtime = models.FloatField(verbose_name='添加时间',blank=True,null=True)
    goods_carts = models.FloatField(verbose_name='商品数量',default=1,blank=True,null=True)
    buyer_id = models.ForeignKey(to=Buyer,verbose_name='买家id',on_delete=models.CASCADE)
    store_id = models.ForeignKey(to=Store,verbose_name='商店id',on_delete=models.CASCADE,default=2)


from django.db.models import Manager

import datetime
class GoodsTypeManage(Manager):
    def addType(self, name, picture='buyer/images/'):
        goods_type = GoodsType()
        goods_type.name = name
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        goods_type.description = '%s_%s'%(now,name)
        goods_type.picture = picture
        goods_type.save()
        return goods_type

class GoodsType(models.Model):
    name = models.CharField(max_length=32,verbose_name='商品类型名称')
    description = models.TextField(max_length=32,verbose_name='商品类型描述')
    picture = models.CharField(max_length=64,verbose_name='商品图片')
    object = GoodsTypeManage()#只适用于GoodsType这个类

class GoodsManage(Manager):
    def up_goods(self):
        '''
        全部上架商品
        :return:
        '''
        return Goods.objects.filter(goods_under = 1)

class Order(models.Model):#订单表
    order_id = models.CharField(max_length=32,verbose_name='订单编号')
    goods_count = models.IntegerField(verbose_name='商品数量')
    order_time = models.IntegerField(verbose_name='订单时间')
    order_price = models.FloatField(verbose_name='订单总价')

    order_address = models.ForeignKey(to=Address,on_delete=models.CASCADE,verbose_name='订单地址')
    order_user = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name='订单所属用户')

class OrderDetail(models.Model):
    goods_id = models.IntegerField(verbose_name='商品id')
    goods_name = models.CharField(max_length=32,verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_number = models.IntegerField(verbose_name='商品购买数量')
    goods_total = models.FloatField(verbose_name='商品总价')
    goods_store = models.IntegerField(verbose_name='商店id')
    goods_order_time = models.IntegerField(verbose_name='商品订单时间')
    goods_image = models.ImageField(verbose_name='商品图')

    order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name='订单编号(多对一)')
