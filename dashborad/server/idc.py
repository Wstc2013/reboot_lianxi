#!/usr/bin/env python
#-*- coding:utf8 -*-
from  django.views.generic import  TemplateView,View,ListView
from  dashborad.models import Idc,Userprofile
from  django.http import JsonResponse,Http404,HttpResponse
from  django.shortcuts import render
from  dashborad.form import IdcForm

class ListIdcView(ListView):

    template_name = 'server/idc.html'
    model = Idc


class AddIdcView(TemplateView):
    template_name = 'server/add_idc.html'
    def get_context_data(self, **kwargs):
        context = super(AddIdcView,self).get_context_data(**kwargs)
        context['user_objs'] = Userprofile.objects.all()
        return  context

    def post(self,request):
        ret = {'status':0,'tips':'添加成功'}
        form_obj = IdcForm(request.POST)
        if form_obj.is_valid():
            form_data = form_obj.cleaned_data
            print form_data
            user_id = form_obj.cleaned_data['idc_user']
            try:
                user_profile_obj =  Userprofile.objects.get(pk=user_id)
            except Userprofile.DoesNotExist as e:
                ret['tips'] = '添加失败'
                ret['status'] = 1
                ret['message'] = str(e)

            else:
                form_data['idc_user'] = user_profile_obj
                Idc.objects.create(**form_data)
        else:
            #print form_obj.errors.as_text()
            ret['message'] = form_obj.errors.as_data()
            ret['tips'] = '格式错误'
            ret['status'] = 1
        return render(request,'server/add_idc.html',ret)