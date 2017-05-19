#!/usr/bin/env python
#-*- coding:utf8 -*-

from  django.views.generic import  TemplateView,View,ListView
from  django.shortcuts import  render
from  django.http import  HttpResponse,JsonResponse
from  dashborad.models import Server,Status,Product
from django.contrib.auth.decorators import permission_required,login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import get_object_or_404
from  django.core import serializers
import  logging
logger = logging.getLogger('opsweb')
import  json


class  get_sever_info_api(View):

    def post(self,request):
        ret = {'status':'update ok'}
        server_ret = request.POST.dict()
        try:
            Server.objects.get(uuid=server_ret['uuid'])
            Server.objects.filter(uuid=server_ret['uuid']).update(**server_ret)
        except Server.DoesNotExist as e:
            s = Server(**server_ret)
            s.save()
            ret['status'] = 'create ok'
        except Exception as e:
            ret['status'] = 'sysinfo fail'
            logger.error('sysinfo 同步失败:{}'.format(str(e)))

        return JsonResponse(ret,safe=True)


class get_server_list_view(ListView):

    template_name = 'server/serverlist.html'
    model = Server    #表名
    paginate_by = 10  ##一页显示多少行
    before_index = 6
    after_index = 5

    def get_context_data(self, **kwargs):
        context = super(get_server_list_view,self).get_context_data(**kwargs)
        context['page_range'] = self.get_page_range(context['page_obj'])
        context['login_user'] = self.request.user
        context.update(self.request.GET.dict())
        arg = self.request.GET.copy()
        if arg.has_key('page'):
            arg.pop('page')
        context['url'] = arg.urlencode()

        return context

    def get_queryset(self):
        queryset = super(get_server_list_view,self).get_queryset()
        queryset = self.get_serach_queryset(queryset)
        return  queryset

    def get_serach_queryset(self,queryset):
        hostname = self.request.GET.get('hostname',None)
        ip = self.request.GET.get('ip', None)
        if hostname:
            hostname = hostname.strip().lower()
            queryset = queryset.filter(hostname__contains=hostname)
        if ip:
            ip = ip.strip().lower()
            queryset = queryset.filter(inner_ip__contains=ip)
        return  queryset

    def get_page_range(self,page_obj):
        start_index = page_obj.number - self.before_index
        if start_index < 0:
            start_index = 0
        return page_obj.paginator.page_range[start_index:page_obj.number + self.after_index]

    @method_decorator(login_required)
    @method_decorator(permission_required("dashborad.view_server",login_url=settings.PERMISSION))
    def get(self, request, *args, **kwargs):
        return super(get_server_list_view,self).get(request, *args, **kwargs)


class ModifyStatusView(TemplateView):
    template_name = 'server/status.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyStatusView,self).get_context_data(**kwargs)
        server_obj = get_object_or_404(Server,pk=self.request.GET.get('server_id',None))
        context['server_obj'] = server_obj
        context['status_obj'] = Status.objects.all()

        return  context

    def post(self,request):
        ret = {'status':0}
        ret['next_url'] = request.GET.get('next','/server/list')
        server_id =  request.POST.get('id',None)
        status_id = request.POST.get('status_id',None)
        try:
            server_obj = Server.objects.get(pk=server_id)
            status_obj = Status.objects.get(pk=status_id)
        except Exception as e:
            ret['status'] = 1
            ret['message'] = str(e)
        else:
            server_obj.status = status_obj.name
            server_obj.save()
        print  ret
        return  render(request,settings.ERROR_TEMPLATE,ret)


class ModifyProductView(TemplateView):
    template_name = 'server/modifyproduct.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyProductView,self).get_context_data(**kwargs)
        context['server_obj'] = get_object_or_404(Server,pk=self.request.GET.get('server_id',None))
        context['product_objs'] = Product.objects.filter(p_product=None)
        return context

    def post(self,request):
        ret = {'status':0,'next_url':'/server/list/'}
        server_id = request.POST.get('id',None)
        business_id = request.POST.get('business_id',None)
        product_id =  request.POST.get('product_id',None)
        try:
            server_obj = Server.objects.get(pk=server_id)
            business_obj = Product.objects.get(pk=business_id)
            product_obj  = Product.objects.get(pk=product_id)
        except Exception as e:
            ret['status'] = 1
            ret['message'] = str(e)
        else:
            server_obj.server_business = business_obj
            server_obj.server_product = product_obj
            server_obj.save()

        return render(request, settings.ERROR_TEMPLATE, ret)

class ProductOptions(View):
    def get(self,request):
        product_id = request.GET.get('product_id',None)
        try:
            p_obj = Product.objects.get(pk=product_id)
        except Product.DoesNotExist as e:
            pass
        else:
            product_objs = Product.objects.filter(p_product=p_obj)
            product_objs = serializers.serialize('json', product_objs)
            return HttpResponse(product_objs)



