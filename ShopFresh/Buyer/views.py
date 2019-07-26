from django.shortcuts import render

# Create your views here.
import hashlib
from django.shortcuts import render
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
                'goods_list':goods_list#每条数据的
            }
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
    return render(request,'buyer/goods_detail.html')












#
# def goodsya(request):
#     goods_type_list = GoodsType.objects.all()
#     goods_list = Goods.objects.all()
#     return render(request,'Buyer/index.html',locals())