#!/usr/bin/env python
#-*- coding:utf8 -*-

from  django.views.generic import  TemplateView,View,ListView
from  dashborad.models import Idc,Userprofile
from  django.http import JsonResponse,Http404,HttpResponse,QueryDict
from  django.shortcuts import render
from  dashborad.models import Server,Product
from  dashborad import  public
import  logging
logger = logging.getLogger('opsweb')
from django.conf import settings
import  json
import  zb,host



class HostRsyncView(TemplateView):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace','search','async']
    template_name = 'zabbix/host_rsync.html'

    def get_context_data(self, **kwargs):
        context = super(HostRsyncView, self).get_context_data(**kwargs)
        context['znodes'] = json.dumps(public.Ztree().get_zabbix())
        context['servers'] = Server.objects.all()[0:10]
        context['groups'] = zb.Zabbix().get_zabbix_group_info()
        return   context

    def search(self,request):
        search_val = QueryDict(request.body).get('search_val',None)
        server_list = []
        if search_val is not None:
            server_list = Server.objects.filter(hostname__contains=search_val).values('id','hostname')[0:10]
            server_list = list(server_list)
        return JsonResponse(server_list,safe=False)


    def async(self,request):
        id = QueryDict(request.body)
        id = id.get('id',None)
        data = []
        try:
            product_obj = Product.objects.get(pk=id)
        except Exception as e:
            print str(e)
        else:

            server_objs = Server.objects.filter(server_product=product_obj)
            for server_obj in server_objs:
                ret = {"name": server_obj.hostname, "id": server_obj.id}
                data.append(ret)
        return JsonResponse(data, safe=False)

    def  post(self,request):
        ret = {'status':0}
        zabbix_hostgroup_id = request.POST.get("group",None)
        server_id_list = request.POST.getlist("server",None)
        server_objs = []
        for server_id in  server_id_list:
            try:
                server_obj = Server.objects.get(pk=server_id)
            except Exception as e:
                ret['message']  = str(e)
            else:
                server_objs.append(server_obj)

        ret['data'] = host.create_host(server_objs,zabbix_hostgroup_id)
        return JsonResponse(ret,safe=True)
