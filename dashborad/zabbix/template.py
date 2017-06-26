#!/usr/bin/env python
#-*- coding:utf8 -*-
from  django.views.generic import  TemplateView,View,ListView
from  dashborad.models import Idc,Userprofile
from  django.http import JsonResponse,Http404,HttpResponse,QueryDict
from  django.shortcuts import render
from  dashborad.models import Server,Product,ZabbixHost
from  dashborad import  public
import  logging
logger = logging.getLogger('opsweb')
from django.conf import settings
import  json
import  zb,host
from dashborad.public import Ztree

class LinktemplateView(TemplateView):
    template_name = 'zabbix/template.html'

    def get_context_data(self, **kwargs):
        context = super(LinktemplateView,self).get_context_data(**kwargs)
        context['templates'] = zb.Zabbix().get_template()
        context['znodes'] = json.dumps(Ztree().get_product())
        return  context


class GetHostStatusView(View):
    def get(self,request):
        ret = {'status':0}
        product_id =  request.GET.get('id',None)
        try:
            product_obj = Product.objects.get(pk=product_id)
        except Exception as e:
            ret['status']  = 1
            ret['message'] =str(e)
        else:
            server_objs = Server.objects.filter(server_product=product_obj)
            ret['data']=host.get_hoststatus(server_objs)

        return  JsonResponse(ret,safe=True)