#!/usr/bin/env python
#-*- coding:utf8 -*-

from  django  import forms
from  dashborad.models import   Product,Userprofile
from dashborad import  models

class Product(forms.Form):
    name = forms.CharField(required=True,max_length=32,
                                    error_messages = {'required': '业务线名称不能为空', 'max_length': '业务线名称长度错误'})
    p_product = forms.CharField(required=True)
    module_letter = forms.CharField(required=True,max_length=10,
                                    error_messages={'required': '业务线英文名称不能为空', 'max_length': '业务线英文名称用户长度错误'})
    op_interface = forms.MultipleChoiceField(choices=((user_obj.name,user_obj.email) for user_obj in Userprofile.objects.all()))
    dev_interface = forms.MultipleChoiceField(choices=((user_obj.name,user_obj.email) for user_obj in Userprofile.objects.all()))

    def clean_p_product(self):
        p_product = self.cleaned_data.get('p_product')
        try:
            p_id = int(p_product)
        except ValueError:
            forms.ValidationError('上级业务线错误')
        else:
            print type(p_id)
            if p_id == 0:
                return None
            try:
                p_obj = models.Product.objects.get(pk=p_id)
                return  p_obj
            except Exception:
                forms.ValidationError('业务线不存在')

    def clean_module_letter(self):
        module_letter = self.cleaned_data.get('module_letter')
        return  module_letter.lower()

    def clean_op_interface(self):
        op_interface = self.cleaned_data.get('op_interface')
        return ','.join(op_interface)

    def clean_dev_interface(self):
        dev_interface = self.cleaned_data.get('dev_interface')
        return ','.join(dev_interface)
