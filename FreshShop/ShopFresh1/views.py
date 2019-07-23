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
    response = render(request,'ShopFresh1/login.html')
    response.set_cookie('login_from','login_page')
    # 访问登入页面时下发一个固定的cookie，
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = Seller.objects.filter(username=username).first()
            user_id = user.id
            if user:
                web_password = set_mima(password)
                cookies = request.COOKIES.get('login_from')
                if user.password == web_password and cookies == 'login_page':
                    # 密码输入正确，并且cookie正确
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie('username',username)
                    # 那么我给这个用户，设置了session，这样他在本站的所有页面就不会再次登录了
                    response.set_cookie('user_id',user_id)
                    request.session['username'] = username
                    return response
    return response

def index(request):
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
    return render(request,'ShopFresh1/register_store.html',locals())

def add_goods(request):
    if request.method =='POST':
        goods_name = request.POST.get('goods_name')
        goods_price= request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_description = request.POST.get('goods_description')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')
        store_id = request.POST.get('store_id')

        goods_image = request.FILES.get('goods_image')

        #保存数据
        goods = Goods()
        goods.goods_name=goods_name
        goods.goods_price = goods_price
        goods.goods_number=goods_number
        goods.goods_description=goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()#对应表有多对多时，保存两次
        # 保存多对多数据
        store_idint = int(store_id)
        goods.store_id.add(
            Store.objects.get(user_id= store_idint)
        )
        goods.save()
    return render(request,'ShopFresh1/add_goods.html')

def list_goods(request):
    keywords = request.GET.get('keywords','')
    page_num = request.GET.get('page_num',1)
    if keywords:
        # 模糊查询
        goods_list = Goods.objects.filter(goods_name__contains=keywords)
    else:
        goods_list = Goods.objects.all()
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,'ShopFresh1/show_goods.html',locals())













def page404(request):
    return render(request,'ShopFresh1/404.html')

def buttons(request):
    return render(request,'ShopFresh1/buttons.html')

def cards(request):
    return render(request,'ShopFresh1/cards.html')

def charts(request):
    return render(request,'ShopFresh1/charts.html')

def tables(request):
    return render(request,'ShopFresh1/tables.html')

def utilltiesanimation(request):
    return render(request,'ShopFresh1/utillties-animation.html')

def utilltiesborder(request):
    return render(request,'ShopFresh1/utillties-border.html')

def utilltiescolor(request):
    return render(request,'ShopFresh1/utillties-color.html')

def utilltiesothor(request):
    return render(request,'ShopFresh1/utillties-other.html')