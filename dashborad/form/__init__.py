#!/usr/bin/env python
#-*- coding:utf8 -*-

from  django  import forms
class IdcForm(forms.Form):
    name = forms.CharField(max_length=10,error_messages={'required':'idc英文名称不能为空','max_length':'idc英文名称用户长度错误'})
    idc_name = forms.CharField(max_length=100)
    idc_address = forms.CharField(max_length=255)
    idc_user = forms.CharField(max_length=32)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return  name.lower()