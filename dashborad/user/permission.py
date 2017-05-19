#!/usr/bin/env python
#-*- coding:utf8 -*-
from  django.views.generic import  TemplateView,ListView,View
from dashborad.models import UserGroup
from django.contrib.auth.models import Group,User,ContentType,Permission
from django.http import  HttpResponse,JsonResponse,QueryDict,Http404
import json
from  django.core import serializers
from  django.conf import  settings
from  django.shortcuts import render

class PermissionView(ListView):
    template_name = 'user/permissionlist.html'
    model = Permission    #表名
    paginate_by = 10  ##一页显示多少行
    before_index = 6
    after_index = 5

    def get_context_data(self, **kwargs):
        context = super(PermissionView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        return  context

    def get_page_range(self,page_obj):
        start_page = page_obj.number - self.before_index
        if start_page < 0:
            start_page = 0
        page_range = page_obj.paginator.page_range[start_page:page_obj.number + self.after_index]
        return  page_range


class  ModifyPermissionView(View):
   def post(self,request):
       ret = {'status':0}
       pid = request.POST.get('pid',None)
       name = request.POST.get('permission_name',None)
       print pid,name
       try:
           permission_obj = Permission.objects.get(pk=pid)
       except Permission.DoesNotExist:
           ret['status']= 1
           ret['message'] = '权限不存在'
       except Exception as e:
           ret['status'] = 2
           ret['message'] = str(e)
       else:
           permission_obj.name = name
           permission_obj.save()
       return JsonResponse(ret,safe=True)



