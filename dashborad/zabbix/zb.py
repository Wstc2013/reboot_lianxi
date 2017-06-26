#!/usr/bin/env python
#-*- coding:utf8 -*-
from zabbix_client import ZabbixServerProxy
from django.conf import settings

class Zabbix(object):

    def __init__(self):
        self.s = ZabbixServerProxy(settings.ZABBIX_URL)
        self.s.user.login(user=settings.ZABBIX_USER, password=settings.ZABBIX_PASS)

    def  get_zabbix_group_info(self):
        ret = self.s.hostgroup.get(output=['groupid', 'name'])
        return  ret

    def create_hosts(self, params):
        return self.s.host.create(**params)

    def get_host(self,hostid):
        ret = self.s.host.getobjects(hostid=hostid)
        return  ret

    def get_template(self, ids=None):
        kwargs = {"output": ['templateid', 'name']}
        if ids:
            kwargs['hostids'] = ids
        ret = self.s.template.get(**kwargs)
        return ret
