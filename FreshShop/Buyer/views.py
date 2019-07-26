import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from Buyer.models import *

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
    return render(request,'Buyer/index.html')