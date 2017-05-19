#!/usr/bin/env python
#-*- coding:utf8 -*-

from django import template
register = template.Library()
@register.simple_tag
def error_message(arg):
     ret = ''
     if arg:
        ret = arg[0][0]
     return  ret