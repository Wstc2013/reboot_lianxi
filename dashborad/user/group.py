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
from  django.contrib.auth.decorators import  login_required,permission_required
from  django.utils.decorators import method_decorator


class GroupView(ListView):
    template_name = 'user/grouplist.html'
    model = Group    #表名
    paginate_by = 10  ##一页显示多少行
    before_index = 6
    after_index = 5

    def get_context_data(self, **kwargs):
        context = super(GroupView,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        return  context

    def get_page_range(self,page_obj):
        start_page = page_obj.number - self.before_index
        if start_page < 0:
            start_page = 0
        page_range = page_obj.paginator.page_range[start_page:page_obj.number + self.after_index]
        return  page_range


    @method_decorator(login_required)
    def post(self,request):
        ret = {'status':0}
        if not request.user.has_perm("auth.add_group"):
            ret['message'] = '没有权限'
            ret['status'] = 2
        else:
            group_name =  request.POST.get('group_name',None)
            try:
                Group.objects.create(name=group_name)
            except Exception as e:
                ret['message'] = str(e)
                ret['status'] = 1
        return  JsonResponse(ret,safe=True)

    @method_decorator(login_required)
    @method_decorator(permission_required("dashborad.view_grouplist",login_url=settings.PERMISSION))
    def get(self, request, *args, **kwargs):
        return super(GroupView,self).get(request, *args, **kwargs)


class UserGroupView(View):
    @method_decorator(login_required)
    def get(self,request):
        ret = {'status':0}
        if not request.user.has_perm("dashborad.view_usergroup"):
            ret['message'] = '没有权限'
            ret['status'] = 2
        else:
            uid =  request.GET.get('uid',None)
            try:
                user_obj = User.objects.get(pk=uid)
                usergroup_obj = user_obj.groups.all()
                group_all_obj = Group.objects.all()
                group_obj = [group for group in group_all_obj if group not in usergroup_obj]
                ret['data'] = serializers.serialize('json', group_obj)

            except User.DoesNotExist:
                ret['message'] = '用户不存在'
                ret['status'] = 1
            except Exception as e:
                ret['message'] = str(e)
                ret['status'] = 2


        return  JsonResponse(ret,safe=True)

    @method_decorator(login_required)
    def post(self,request):
        ret = {'status': 0}
        if not request.user.has_perm("dashborad.add_usergroup"):
            ret['message'] = '没有权限'
            ret['status'] = 2
        else:
            uid =  request.POST.get('user_id')
            group_id =  request.POST.get('group_id')
            try:
                user_obj = User.objects.get(pk=uid)
                group_obj = Group.objects.get(pk=group_id)
                user_obj.groups.add(group_obj)
            except User.DoesNotExist,Group.DoesNotExist:
                ret['message'] = '用户或用户组不存在'
                ret['status'] = 1
            except Exception as e:
                ret['message'] = str(e)
                ret['status'] = 2
        return  JsonResponse(ret,safe=True)

class GroupUserView(View):
    @method_decorator(login_required)
    def get(self,request):
        ret = {'status': 0}
        if not request.user.has_perm("dashborad.view_groupuser"):
            ret['message'] = '没有权限'
            ret['status'] = 2
        else:
            gid =  request.GET.get('gid',None)
            try:
                group_obj = Group.objects.get(pk=gid)
                group_user_obj = group_obj.user_set.all()
                ret['data'] = serializers.serialize('json', group_user_obj)
            except Group.DoesNotExist:
                ret['message'] = '用户组不存在'
                ret['status'] = 1
            except Exception as e:
                ret['message'] = str(e)
                ret['status'] = 2
        return JsonResponse(ret, safe=True)

    @method_decorator(login_required)
    def delete(self,request):
        ret = {'status':0}
        if not request.user.has_perm("dashborad.del_groupuser"):
            ret['message'] = '没有权限'
            ret['status'] = 2
            data = QueryDict(request.body)
            gid = data.get('groupid',None)
            uid = data.get('userid',None)
            try:
                user_obj = User.objects.get(pk=uid)
                group_obj = Group.objects.get(pk=gid)
                group_obj.user_set.remove(user_obj)
            except User.DoesNotExist,Group.DoesNotExist:
                ret['message'] = '用户或用户组不存在'
                ret['status'] = 1
            except Exception as e:
                ret['message'] = str(e)
                ret['status'] = 2
        return  JsonResponse(ret,safe=True)

class Groupermission(TemplateView):
     template_name = 'user/groupermission.html'


     def get_context_data(self, **kwargs):
         context = super(Groupermission,self).get_context_data(**kwargs)
         context['group_permissions'] = self.group_permission()
         context['content_type'] = ContentType.objects.all()
         context['group'] =  self.request.GET.get('gid', None)
         return  context

     def group_permission(self):
         gid = self.request.GET.get('gid', None)
         try:
             group_obj = Group.objects.get(pk=gid)
             group_permission = [ permission.id for permission in group_obj.permissions.all()]
             return  group_permission
         except Group.DoesNotExist:
             raise Http404

     def get(self, request, *args, **kwargs):
         return super(Groupermission,self).get(request, *args, **kwargs)

     def post(self,request):
        ret = {'status':0,'next_url':'/group/list'}
        permission_id_list = request.POST.getlist('permission',[])
        groupid = request.POST.get('group',None)
        try:
            group = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['message'] ='用户组不存在'
        else:
            if permission_id_list:
                permission_objs = Permission.objects.filter(id__in=permission_id_list)
                group.permissions = permission_objs
        return  render(request,settings.ERROR_TEMPLATE,ret)


class GroupPermissionlist(View):
    def get(self,request):
        ret = {'status':0}
        gid = request.GET.get('gid',None)
        try:
            group_obj = Group.objects.get(pk=gid)
            group_permission = [{'id':permission.id,'name':permission.codename} for permission in group_obj.permissions.all()]
            ret['data'] = group_permission
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['message'] = "用户组不存在"
        return JsonResponse(ret,safe=True)
