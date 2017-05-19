#-*-coding:utf8-*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import  JsonResponse,HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import  settings
from django.template import Context,loader
# Create your views here.
import  logging
logger = logging.getLogger('opsweb')

def login_view(request):
    if request.method == 'GET':
        return  render(request,'user/login.html')
    elif request.method == "POST":
        ret = {'status':0}
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                #request.session.set_expiry(10)
                ret['next_url'] = '/'
            else:
                ret['status'] = 1
                ret['errmsg'] = '用户被禁用'
        else:
            ret['status'] = 2
            ret['errmsg'] = '用户名或密码错误'
        return  JsonResponse(ret,safe=True)

class IndexView(View):
    @method_decorator(login_required)
    def get(self,request):
        #print request.user.has_perm('dashborad.change_department')
        return  render(request, "public/index.html",{'login_user':request.user})

def logout_view(request):
    logout(request)
    return HttpResponse('退出成功')

def permission(request):
    return render(request,'public/permission.html')

