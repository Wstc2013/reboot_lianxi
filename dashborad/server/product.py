#!/usr/bin/env python
#-*- coding:utf8 -*-

from  django.views.generic import  TemplateView,View,ListView
from  dashborad.models import Idc,Userprofile
from  django.http import JsonResponse,Http404,HttpResponse
from  django.shortcuts import render
from  dashborad.form.product import Product
from  dashborad import  models
from  dashborad.models import Server
import  logging
logger = logging.getLogger('opsweb')
from django.conf import settings
import  json

class Ztree(object):

    def __init__(self):
        self.data = self._get_all_data()

    def _get_all_data(self):
        product_objs = models.Product.objects.all()
        return  product_objs

    def _get_second_product_obj(self,pid):
        second_product = [  objs for objs in self.data if objs.p_product is not None and objs.p_product.id ==pid]
        return  second_product

    def get(self):
        ret = []
        one_product = [  objs for objs in self.data if objs.p_product is None]
        for one_obj in one_product:
            second_product = self._get_second_product_obj(one_obj.id)
            tmp = {}
            tmp['pid'] = 0
            tmp['id'] =one_obj.id
            tmp['name'] = one_obj.name
            tmp['children'] =[]
            for child in second_product:
                tmp['children'].append({"pid":one_obj.id,"name":child.name,"id":child.id})
            ret.append(tmp)
        return ret






class AddProductView(TemplateView):

     template_name = 'server/product.html'

     def get_context_data(self, **kwargs):
         context = super(AddProductView,self).get_context_data(**kwargs)
         context['user_objs'] = Userprofile.objects.all()
         #context['product_objs'] =models.Product.objects.all()
         context['product_objs'] = models.Product.objects.filter(p_product__isnull=True)
         return context

     def post(self, request):
         ret = {'status': 0, "next_url": ''}
         print request.POST
         form_obj = Product(request.POST)
         if form_obj.is_valid():
             try:
                 form_data = form_obj.cleaned_data
                 print form_data
                 Product_obj = models.Product(**form_data)
                 Product_obj.save()
                 #logger.error('cheshi')
             except Exception as e:
                 msg = "用户{}添加业务线出错:{}".format(request.user.username, e.args)
                 logger.error(msg)
                 ret['status'] = 1
                 ret['message'] = msg
         else:
             # print form_obj.errors.as_text()
             msg = "用户{}添加业务线验证失败:{}".format(request.user.username, form_obj.errors.as_json())
             logger.error(msg)
             ret['message'] = msg
             ret['status'] = 1
         # return render(request,settings.ERROR_TEMPLATE , ret)
         print ret
         return HttpResponse('')

class  ListProductView(TemplateView):
    template_name = 'server/product_manage.html'


    def get_context_data(self, **kwargs):
        context = super(ListProductView, self).get_context_data(**kwargs)
        context['znodes'] = json.dumps(Ztree().get())
        #context['znodes'] = Ztree().get()
        return   context

class  ListNodeInfoView(View):

    def get(self,request):
        ret = {'status':0}
        id = request.GET.get('id',None)
        try:
            product_ret = models.Product.objects.get(pk=id).__dict__


        except models.Product.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = '业务线不存在'
        else:
            p_product_id = product_ret['p_product_id']
            if p_product_id:
                pname = models.Product.objects.get(pk=p_product_id).name
            else:
                pname = '顶级业务线'
            product_ret['p_product_id'] = pname
            del product_ret['_state']
            ret['data'] = product_ret
        return  JsonResponse(ret,safe=True)


class  ModifiyView(View):

    def post(self,request):
        ret = {'status':0}
        print request.POST
        product_id = request.POST.get('id',None)
        service_name = request.POST.get('service_name',None)
        module_letter = request.POST.get('module_letter',None)
        dev_interface = request.POST.getlist('dev_interface[]',None)
        op_interface = request.POST.getlist('op_interface[]', None)

        try:
            product_obj = models.Product.objects.get(pk=product_id)
            print product_obj.name, product_obj.module_letter
            if  product_obj.dev_interface != ','.join(dev_interface):
                 product_obj.dev_interface = ','.join(dev_interface)
            if  product_obj.op_interface != ','.join(op_interface):
                 product_obj.op_interface = ','.join(op_interface)
            if product_obj.name != service_name:
                 product_obj.name = service_name
            if product_obj.module_letter != module_letter:
                 product_obj.module_letter = module_letter
            product_obj.save()
            print product_obj.name,product_obj.module_letter
        except models.Product.DoesNotExist as e:
            ret['status'] = 1
            ret['message'] = '业务线不存在'


        return  JsonResponse(ret,safe=True)


class HostListView(View):
    def get(self,request):
        ret = {'status':0}
        product_id = request.GET.get('id',None)
        try:
            product_obj = models.Product.objects.get(pk=product_id)
        except Product.DoesNotExist as e:
            ret['status'] = 1
            ret['message'] = str(e)
        else:
            server_ip = [  {"ip":server_obj.inner_ip,"name":server_obj.hostname} for  server_obj in Server.objects.filter(server_product=product_obj)]
            ret['data'] = json.dumps(server_ip)
        return JsonResponse(ret,safe=True)

