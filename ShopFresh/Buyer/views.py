from django.shortcuts import render
import time
# Create your views here.
import hashlib
from django.shortcuts import render,HttpResponse
from django.shortcuts import HttpResponseRedirect
from Buyer.models import *
from ShopFresh1.models import Goods,GoodsType

def set_password(password):
    request = hashlib.md5()
    request.update(password.encode())
    return request.hexdigest()

def LoginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get('username')
        s_user = request.COOKIES.get('username')
        if c_user and s_user and c_user==s_user:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/buyer/login/')
    return inner
# Create your views here.
def register(request):
    if request.method=='POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect('/buyer/login/')
    return render(request,'Buyer/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user:
                password_db = set_password(password)
                if user.password == password_db:
                    response = HttpResponseRedirect('/buyer/index/')
                    # 登录校验
                    response.set_cookie('username',user.username)
                    request.session['username'] = user.username
                    # 设置session
                    response.set_cookie('user_id',user.id)
                    return response
    return render(request,'Buyer/login.html')

def logout(request):
    response = HttpResponseRedirect('/buyer/index/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session['username']
    return response


@LoginValid
def index(request):
    result_list = []
    goods_type_list = GoodsType.objects.all()#获得商品类型的所有类型
    for good_type in goods_type_list:
        # 遍历所有数据，得到每条数据
        goods_list = good_type.goods_set.values()[:4]
        # 反向查询每条数据对应的从表中的数据，前四条
        if goods_list:
            # 如果有数据
            goodType = {
                'id':good_type.id,#每条数据的id
                'name':good_type.name,#每条数据的name
                'picture':good_type.picture,#每条数据的图片
                'description':good_type.description,#每条数据的描述
                'goods_list':goods_list#每条数据的所有形成一个字典
            }
            # print(goods_list)
            result_list.append(goodType)#放在一个列表中
    # print(result_list)
    return render(request,'Buyer/index.html',locals())


@LoginValid
def goods_list(request):
    goodsList = []
    type_id = request.GET.get('type_id')#请求过来数据中所有的类型id
    goods_type = GoodsType.objects.filter(id = type_id).first()
    # 按照类型id从数据库中进行查找
    if goods_type:
        goodsList = goods_type.goods_set.filter(goods_under=1)
        # 找到所有的商品
    return render(request,'buyer/goods_list.html',locals())

@LoginValid
def goods_detail(request):
    # 这个页面的路由跳转不过去
    goods_id = request.GET.get('goods_id')
    # goods_id = int(goods_id)
    # 弄了半天原来是获取不到货物的id
    # name = int(name)
    goods_data = Goods.objects.filter(id=goods_id).first()

    return render(request, 'buyer/goods_detail.html', locals())


# 支付函数
import time
from alipay import AliPay
def pay_order(request):
    money = request.GET.get('money')
    order_id = request.GET.get('order_id')
    moretime = int(time.time())
    order_ids = str(moretime) + order_id
    # 如果用时间戳，当是否页面跳转的时间会发生改变
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsUz6B1oA0tJkDIg3nvKbUggu3FswnBQ6e5kj1MSxrbAKJF1s2+6fK0tpBD5VWaRCyKCf73ulC0BQv2WFKRxQ+ud3r08JuKr0a6u2aBnua7+Zbw34kbqoNYJ0LZitGdJQnotbDc2GgyxOO2Bd3WjvInB4otjXS2y3jNDQRh2fV2Rml4C5RcTIsbeivcvNw3/pvNTP6x45neD1JpPxeFvgT/Y9aj/Xytw52mYLycblZ++fto48zzCSrxKzotyJR5b5shFdOjheTKb1SMGAiXKh03MmRjMqwR8iNn/7j9oreCykzxKcSewrshXpnjslBqZDlpWoUGJU09kfhMiO1espKwIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAsUz6B1oA0tJkDIg3nvKbUggu3FswnBQ6e5kj1MSxrbAKJF1s2+6fK0tpBD5VWaRCyKCf73ulC0BQv2WFKRxQ+ud3r08JuKr0a6u2aBnua7+Zbw34kbqoNYJ0LZitGdJQnotbDc2GgyxOO2Bd3WjvInB4otjXS2y3jNDQRh2fV2Rml4C5RcTIsbeivcvNw3/pvNTP6x45neD1JpPxeFvgT/Y9aj/Xytw52mYLycblZ++fto48zzCSrxKzotyJR5b5shFdOjheTKb1SMGAiXKh03MmRjMqwR8iNn/7j9oreCykzxKcSewrshXpnjslBqZDlpWoUGJU09kfhMiO1espKwIDAQABAoIBAQCf7JkSjIJ1p0SLcUsKWjbzdWIfbTmZbz2ZQvbo8kp6KnHbf1Gzx7dWq/yb0UXXR6zdntTkhRjH30l2erHz9RCuYJ66SIayRbGWdRphKBLAqeBSJb3yZPVY3sTAZBivU99YQsbs2lfcddhTAodoMUCSRfTqnsEDzZp6r9dNh2a0weA38JKHr16VHLtQ1U7mzpyjvyWUNQSpeyPw2crl2Xo/WobnhJW9MsPsmtgRg9HtBfBaOCz68t4EwCWaviIYZ8VBiu/h1v8QFoE8bY3M6ClrUGxy/G86KwdFF5V+OrQ1Aw+4o2wn4POERdtsdh94HZNUhLjgCFXsSUfh8bQJVmGBAoGBAOGW6jqCJkYk6yIrlOX1wP+vWwRqqy+jKB27+b+d6D5kEN8/MrWP9uATcBnOcfSETBVCrzKD4z+8nhdUdqHGOEwK0b6Cu1QwK5byRQTuc4D9L3JfnXR5tOAVQB594X87Yc7b7DThU8qO6IIkXXzATCmycCBbVbIUX+1XevXI7z4LAoGBAMkznc2fn6BIK5MgGZ1F9ztjgjmoeGe59Eb/xGbp4C7sNoxm0OXn0LBU45SctVWQT0l+Iez6y+vI6mAzvWwkH6SzWPBzDV///zriJSsAhhGfF9WqLXSzwd59lUln2vRIZsucDm9T9ZpW7BmO5+vSnbaOHUeQ/VTfQ3pzGxO04VVhAoGABxLbX2BLYPGxac3iCl/tYFcYTIgnvAOqs1v8ldSWvrYWjVmG9oiAHkCdyEFf82HenOANbFEUZCA++M5ONf5oL4I7V3Tz+MzV4RLRtTjg6E+IGFcFMezLDie8bfhWhM3Q4FKnEnVqUjSu9726LLo+6SPOPkV+52maJHAUy/Y0AkcCgYB5BjhMoFCHPAIh/HQL2zMMoR2LCyBp3DvonR6JfPKhpupk58+OCzPHbTh7gwu8TRK0NU+42V7iFDeO6HBvZQc3rb243KvV7AmdZLxQsn7yiIzws+2lvh7GcyniPrtAp3BV1ygDpTAdx107Pm+YtVayoadRDhCkBav0Mtq9rta/4QKBgBjJoQsbs0YNTWgsPJB+Sj3j2g/0EGgVkbuf8M89VKc9RnKpgRxCRRqcJu/gVQHR5OvHkUen1mJwXwRIRRDfbo1bFdlVRJswXox05kTXQZRNxOQ0FJPAIxp47xTMnvUQnPR8KKBIaR56evBkkBGzCzvly98MntNn5Wn5l2XRPLUG
    -----END RSA PRIVATE KEY-----"""

    alipay = AliPay(
        appid='2016101000652494',
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2'
    )
    # 网页支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_ids,  # 订单号,
        total_amount=str(money),  # 支付金额
        subject='生鲜交易',
        return_url='http://127.0.0.1/buyer/pay_result/',
        notify_url='http://127.0.0.1/buyer/pay_result/'
    )
    # 给定的支付宝网关
    return HttpResponseRedirect('https://openapi.alipaydev.com/gateway.do?' + order_string)
    #     支付宝支付遇到了问题，订单显示失败
def pay_result(request):

    return HttpResponse('支付成功')

# 加入购物车
@LoginValid
def cart_add(request):
    user_id = request.COOKIES.get('user_id')
    cart_add_id = request.GET.get('add_id')
    # print(user_id,type(user_id))
    # print(cart_add_id,type(cart_add_id))
    goods = Goods.objects.filter(id=cart_add_id).first()
    goods_image1 = goods.goods_image#图片
    goods_name1 = goods.goods_name#名字
    goods_price1 = goods.goods_price#价格
    goods_carts1 = goods.goods_number#数量
    goods_under1 = goods.goods_under
    addtimes = time.time()
    addtimes = int(addtimes)
    user_id = int(user_id)
    cart_add_id = int(cart_add_id)
    cart_db = Cart()
    cart_db.buyer_id_id =user_id
    # cart_db.user_id = user_id#保存买家信息
    cart_db.goods_id = cart_add_id#保存商品id
    cart_db.goods_name = goods_name1#商品名
    cart_db.goods_price = goods_price1#商品价格
    cart_db.goods_image = goods_image1#图片
    cart_db.goods_carts = goods_carts1#库存
    cart_db.goods_addtime = addtimes#添加时间
    cart_add.goods_under = goods_under1#商品状态
    cart_db.save()
    return render(request,'buyer/goods_detail.html',locals())

# 购物车
def cart(request):
    user_id = request.COOKIES.get('user_id')
    goods = Cart.objects.filter(buyer_id=user_id)
    # goods = Cart.objects.filter( b= user_id).first()#查出这个货物
    return render(request,'buyer/cart.html',locals())





        #
# def goodsya(request):
#     goods_type_list = GoodsType.objects.all()
#     goods_list = Goods.objects.all()
#     return render(request,'Buyer/index.html',locals())