# Create your models here.
from django.db import models
# Create your models here.

class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    email = models.EmailField(verbose_name='用户邮箱')
    phone = models.CharField(max_length=32,verbose_name='联系电话',blank=True,null=True)
    connect_address = models.TextField(verbose_name='联系地址',blank=True,null=True)

class Address(models.Model):
    address = models.TextField(verbose_name='收货地址')
    recver = models.CharField(max_length=32,verbose_name='收件人')
    recver_num = models.CharField(max_length=32,verbose_name='收件人电话')
    post_num = models.CharField(max_length=32,verbose_name='邮编')
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
    goods_name = models.CharField(max_length=32, verbose_name='商品名称',blank=True,null=True)
    goods_price = models.FloatField(verbose_name='商品价格',blank=True,null=True)
    goods_image = models.ImageField(upload_to='shopfresh1/images', verbose_name='商品图片',blank=True,null=True)

    goods_under = models.IntegerField(verbose_name='商品状态', default=1)
    goods_addtime = models.FloatField(verbose_name='添加时间',blank=True,null=True)
    goods_carts = models.FloatField(verbose_name='商品数量',default=1,blank=True,null=True)
    buyer_id = models.ForeignKey(to=Buyer,verbose_name='买家id',on_delete=models.CASCADE)