from django.db import models

# Create your models here.
class Seller(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    nickname = models.CharField(max_length=32,verbose_name='昵称',blank=True)#blank=True,用于字符串
    phone    = models.CharField(max_length=32,verbose_name='电话')
    email    = models.EmailField(max_length=32,verbose_name='邮箱',null=True)#null=True,用于数字
    picture  = models.ImageField(upload_to='shopfresh1/images',verbose_name='头像',blank=True,null=True)
    address  = models.CharField(max_length=32, verbose_name='地址', blank=True)  # blank=True,用于字符串
    card_id  = models.CharField(max_length=32,verbose_name='身份证号',blank=True,null=True)

class StoreType(models.Model):
    store_type = models.CharField(max_length=32,verbose_name='类型名称')
    type_description = models.TextField(verbose_name='类型描述')

class Store(models.Model):
    store_name = models.CharField(max_length=32,verbose_name='店铺名称')
    store_address = models.CharField(max_length=32,verbose_name='店铺地址')
    store_description = models.TextField(verbose_name='店铺描述')
    store_logo = models.ImageField(upload_to='shopfresh1/images',verbose_name='店铺logo')
    store_phone = models.CharField(max_length=32,verbose_name='店铺电话')
    store_money = models.FloatField(verbose_name='店铺注册资金')
    user_id = models.IntegerField(verbose_name='店铺主人')
    type = models.ManyToManyField(to=StoreType,verbose_name='店铺类型')

class Goods(models.Model):
    goods_name = models.CharField(max_length=32,verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_image = models.ImageField(upload_to='shopfresh1/images',verbose_name='商品图片')
    goods_number = models.IntegerField(verbose_name='商品库存')
    goods_description = models.TextField(verbose_name='商品描述')
    goods_date = models.DateField(verbose_name='出厂日期')
    goods_safeDate = models.IntegerField(verbose_name='保质期')
    store_id = models.ManyToManyField(to=Store,verbose_name='商品店铺')

class GoodsImg(models.Model):
    img_address = models.ImageField(upload_to='shopfresh1/images',verbose_name='图片地址')
    img_description = models.TextField(max_length=32,verbose_name='图片描述')
    goods_id = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name='商品id')
