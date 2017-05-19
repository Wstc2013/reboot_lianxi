#!/usr/bin/env python
#-*- coding:utf8 -*-
from  django.views.generic import  TemplateView,View,ListView
from  django.contrib.auth.models import User
from  django.http import JsonResponse,Http404,HttpResponse
from  django.core.paginator import Paginator
from  dashborad.models import Department,Userprofile
from django.shortcuts import redirect, get_object_or_404,render
from django.conf import settings
from django.contrib.auth.decorators import permission_required,login_required
from django.utils.decorators import method_decorator
from  django.core import serializers
import  json


class  UserListView(TemplateView):
    template_name = 'user/userlist.html'
    before_index = 6
    after_index = 5

    def get_context_data(self, **kwargs):
        context =  super(UserListView,self).get_context_data(**kwargs)
        #context['userlist'] = User.objects.all() ##获取所有用户列表对象
        userlist = User.objects.all()
        paginator = Paginator(userlist,10)
        page = self.request.GET.get('page',1)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(1)
        context['page_obj'] = page_obj
        start_index = page_obj.number - self.before_index
        if start_index < 0:
             start_index = 0
        context['page_range'] = page_obj.paginator.page_range[start_index:page_obj.number + self.after_index]
        return context

    def get(self, request, *args, **kwargs):
        self.request = request
        #TemplateView.get(self,request,*args,**kwargs)
        #self.get(request,*args,**kwargs)
        return super(UserListView,self).get(request, *args, **kwargs)


class USERLISTVIEW(ListView):
    template_name = 'user/userlistl.html'
    model = User    #表名
    paginate_by = 10  ##一页显示多少行
    before_index = 6
    after_index = 5


    def get_context_data(self, **kwargs):
        context = super(USERLISTVIEW,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        user_name = self.request.GET.dict()
        #print type(user_name)
        context.update(user_name)
        context['login_user'] = self.request.user


        return context
    def get_queryset(self):
        queryset = super(USERLISTVIEW,self).get_queryset()
        user_name = self.request.GET.get('name',None)
        if user_name:
            queryset = queryset.filter(username__contains=user_name)
        return  queryset

    def get_page_range(self,page_obj):
        start_index = page_obj.number - self.before_index
        if start_index < 0:
            start_index = 0
        return page_obj.paginator.page_range[start_index:page_obj.number + self.after_index]

    @method_decorator(login_required)
    @method_decorator(permission_required("dashborad.view_userlist",login_url=settings.PERMISSION))
    def get(self, request, *args, **kwargs):
        return super(USERLISTVIEW,self).get(request, *args, **kwargs)



class ModifyUserStatusView(View):
    def post(self,request):
        ret = {'status':0}
        user_id = request.POST.get('user_id',None)
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '用户不存在'
        return JsonResponse(ret,safe=True)


class ModifyDepartmentView(TemplateView):
    template_name = 'user/department.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyDepartmentView,self).get_context_data(**kwargs)
        context['department_obj']  = Department.objects.all()
        #try:
            #context['user_obj'] = User.objects.get(pk=self.request.GET.get('user',None))
            #return context['user_obj']
        #except Exception as e:
            #raise Http404
        #等价于get_object_or_404
        context['user_obj'] = get_object_or_404(User,pk=self.request.GET.get('user', None))
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required("dashborad.change_department", login_url=settings.PERMISSION))
    def get(self, request, *args, **kwargs):
        self.request = request
        return super(ModifyDepartmentView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    @method_decorator(permission_required("dashborad.change_department", login_url=settings.PERMISSION))
    def post(self,request):
        user_id =  request.POST.get('id',None)
        department_id = request.POST.get('department',None)
        if not user_id or not department_id:
            raise  Http404
        try:
            userprofile_obj = Userprofile.objects.get(user__id=user_id)
            department_obj = Department.objects.get(pk=department_id)
            userprofile_obj.department = department_obj
            userprofile_obj.save()
        except Exception as e:
            raise  Http404
        return redirect("/user/userlist/")

class  ModifyPhoneView(TemplateView):
    template_name = 'user/phone.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyPhoneView,self).get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(User,pk=self.request.GET.get('user',None))
        return context


    def get(self, request, *args, **kwargs):
        self.request = request
        return super(ModifyPhoneView,self).get(request, *args, **kwargs)

    def post(self,request):
        ret = {'message':'','status':0,'next_url':"/user/userlist/"}
        user_id = request.POST.get('id', None)
        phone = request.POST.get('phone', None)
        if  len(phone)==11 or  user_id or  phone:

            try:
                userprofile_obj = Userprofile.objects.get(user__id=user_id)
                userprofile_obj.phone = phone
                userprofile_obj.save()
            except Exception as e:
                ret['message'] = str(e)
                ret['status'] = 2
        else:
            ret['message'] = 'user_id或phone不能为空'
            ret['status'] = 1
        return render(request,settings.ERROR_TEMPLATE,ret)

class ProfilelistView(View):

    def get(self,request):
        profile_obj = Userprofile.objects.all().values('name','email')
        profile_obj = list(profile_obj)
        profile_obj = json.dumps(profile_obj)
        return  HttpResponse(profile_obj)