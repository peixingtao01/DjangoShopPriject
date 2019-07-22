import hashlib

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
            if user:
                web_password = set_mima(password)
                cookies = request.COOKIES.get('login_from')
                if user.password == web_password and cookies == 'login_page':
                    # 密码输入正确，并且cookie正确
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie('username',username)
                    # 那么我给这个用户，设置了session，这样他在本站的所有页面就不会再次登录了
                    request.session['username'] = username
                    return response
    return response

def index(request):
    return render(request,'ShopFresh1/index.html')

def page404(request):
    return render(request,'ShopFresh1/404.html')