#
import hashlib
from django.core.paginator import Paginator#分页的包
from django.shortcuts import render,HttpResponseRedirect

from ShopFresh1.models import *

def set_mima(request):
    md5 = hashlib.md5()
    md5.update(request.encode())
    return md5.hexdigest()

# Create your views here.
def register(request):
    #注册
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = set_mima(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect('/store/login/')
    return render(request,'ShopFresh1/register.html')

def login(request):
    # 登入
    response = render(request,'ShopFresh1/login.html')
    response.set_cookie('login_from','login_page')
    # 访问登入页面时下发一个固定的cookie，
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = Seller.objects.filter(username=username).first()
            # 1、先校验用户是否存在
            user_id = user.id
            if user:
                web_password = set_mima(password)
                # 2、验证密码是否正确
                cookies = request.COOKIES.get('login_from')
                # 3、请求是否来自登录页面
                if user.password == web_password and cookies == 'login_page':
                    # 密码输入正确，并且cookie正确
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie('username',username)
                    # 那么我给这个用户，设置了session，这样他在本站的所有页面就不会再次登录了
                    response.set_cookie('user_id',user_id)
                    request.session['username'] = username
                    store = Store.objects.filter(user_id=user_id).first()#查询店铺是否存在
                    if store:
                        response.set_cookie('has_store',store.id)
                        # 有店铺如果存在下发一个属于自己本身的cookie，这个的目的是为了显示前端的店铺页面
                    else:
                        response.set_cookie('has_store','')
                        #  没有店铺，那个下发一个空的cookie，就是为了前端页面进行判断的
                    return response
    return response

def index(request):
    # 首页
    user_id = request.COOKIES.get('user_id')
    if user_id:
        user_ida = int(user_id)
    else:
        user_ida = 0
    store = Store.objects.filter(user_id=user_ida).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,'ShopFresh1/index.html',{'is_store':is_store})

def register_store(request):
    # 注册店铺
    type_list = StoreType.objects.all()
    if request.method =='POST':
        post_data = request.POST
        store_name = post_data.get('store_name')
        store_description = post_data.get('store_description')
        store_phone = post_data.get('store_phone')
        store_money = post_data.get('store_money')
        store_address = post_data.get('store_address')

        # 通过cookie获得user_id
        user_id = int(request.COOKIES.get('user_id'))
        type_lists = post_data.getlist('type')#通过request.post得到，但是得到一个列表

        store_logo = request.FILES.get('store_logo')#通过上传文件，request.FILES得到

        # 保存不是多对多的数据
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()

        for i in  type_lists:
            store_type = StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
        return HttpResponseRedirect('/store/index/')
    return render(request,'ShopFresh1/register_store.html',locals())

def add_goods(request):
    # 增加商品
    type_list = StoreType.objects.all()
    if request.method =='POST':
        goods_name = request.POST.get('goods_name')
        goods_price= request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_description = request.POST.get('goods_description')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')
        store_id = request.POST.get('store_id')#过得店铺id
        goods_image = request.FILES.get('goods_image')

        goods_store = request.COOKIES.get('has_store')
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
        goods_type1 = request.POST.get('goodstype')
        goods_type1 = int(goods_type1)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #保存数据
        goods = Goods()
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
        goods.goods_type = GoodsType.objects.get(id=goods_type1)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
        goods.goods_name=goods_name
        goods.goods_price = goods_price
        goods.goods_number=goods_number
        goods.goods_description=goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.store_id =Store.objects.get(id = int(store_id))#添加了商品店铺的id

        goods.save()#对应表有多对多时，保存两次
        # 保存多对多数据
        # store_idint = int(goods_store)
        # goods.store_id.add(
        #     Store.objects.get(user_id= store_idint)
        # )
        # goods.save()
    return render(request,'ShopFresh1/add_goods.html',locals())

def list_goods(request,state):
    # 判断商品在售情况
    if state=='up':
        state_num =1
    else:
        state_num=0

    # 商品列表
    keywords = request.GET.get('keywords','')
    page_num = request.GET.get('page_num',1)
    # 新增
    store_id = request.COOKIES.get('has_store')
    store_id = int(store_id)
    store = Store.objects.get(id=store_id)
    if keywords:
        # 模糊查询,判断关键字是否存在
        goods_list = store.goods_set.filter(goods_name__contains=keywords,goods_under=state_num)
        # goods_list = Goods.objects.filter(goods_name__contains=keywords)
    else:#不存在查询搜索
        goods_list = store.goods_set.filter(goods_under=state_num)
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,'ShopFresh1/show_goods.html',locals())

def under_goods(request):
    id = request.GET.get('id')
    referer = request.META.get('HTTP_REFERER')
#     获得当前请求的地址来源
    if id:
        goods = Goods.objects.filter(id =id).first()
        goods.goods_under = 0
        goods.save()
    return HttpResponseRedirect(referer)

def goods_detail(request,goods_id):
    # 商品细节
    goods_data = Goods.objects.filter(id = goods_id).first()
    return render(request,'shopfresh1/goods_detail.html',locals())


def goods_update(request,goods_id):
    # 更新商品
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method=='POST':
        # goods_id = request.POST.get('goods_id')
        goods_name =request.POST.get('goods_name')
        goods_image = request.FILES.get('goods_image')
        goods_price = request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_description = request.POST.get('goods_description')
        goods = Goods.objects.get(id = int(goods_data.id))
        if goods_name:
            goods.goods_name = goods_name
            goods.save()
        if goods_price:
            goods.goods_price = goods_price
            goods.save()
        if goods_number:
            goods.goods_number = goods_number
            goods.save()
        if goods_description:
            goods.goods_description = goods_description
            goods.save()
        if goods_image:
            goods.goods_image = goods_image
            goods.save()
        return HttpResponseRedirect('/store/goods_detail/'+str(goods_data.id)+'/')
    return render(request,'shopfresh1/goods_update.html',locals())


def set_goods(request,state):
    if state=='up':
        state_num =1
    else:
        state_num=0
    id = request.GET.get('id')
    referer = request.META.get('HTTP_REFERER')
    if id:
        goods = Goods.objects.filter(id = id).first()
        if state == 'delete':
            goods.delete()
        else:
            goods.goods_under = state_num
            goods.save()
    return HttpResponseRedirect(referer)

def logout(request):
    response = HttpResponseRedirect('/store/index/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session['username']
    return response


# API
from rest_framework import viewsets
from ShopFresh1.serializers import UserSerializer,GoodsTypeSerializer
from ShopFresh1.serializers import *
from django_filters.rest_framework import DjangoFilterBackend #过滤器
class UserViewSet(viewsets.ModelViewSet):
    # 返回具体的查询内容
    queryset = Goods.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]#采用哪个过滤器
    filterset_fields = ['goods_name','goods_price']#需要查询的字段

class TypeViewSet(viewsets.ModelViewSet):
    # 返回具体查询的内容
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer

def ajax_api(request):
    return render(request,'shopfresh1/ajax_API_list_goods.html',locals())

from django.core.mail import send_mail
def sendMail(request):
    send_mail('邮件主题','邮件内容','from_email',['to_email'],fail_silently=False)



from CeleryTask.tasks import add
from django.http import JsonResponse
def get_add(requset):
    add.delay(2,3)
    return JsonResponse({'statue':200})

        #
# def page404(request):
#     return render(request,'ShopFresh1/404.html')
#
# def buttons(request):
#     return render(request,'ShopFresh1/buttons.html')
#
# def cards(request):
#     return render(request,'ShopFresh1/cards.html')
#
# def charts(request):
#     return render(request,'ShopFresh1/charts.html')
#
# def tables(request):
#     return render(request,'ShopFresh1/tables.html')
#
# def utilltiesanimation(request):
#     return render(request,'ShopFresh1/utillties-animation.html')
#
# def utilltiesborder(request):
#     return render(request,'ShopFresh1/utillties-border.html')
#
# def utilltiescolor(request):
#     return render(request,'ShopFresh1/utillties-color.html')
#
# def utilltiesothor(request):
#     return render(request,'ShopFresh1/utillties-other.html')