#!/usr/bin/env python
#-*- coding:utf8 -*-
from dashborad.zabbix.zb import  Zabbix
from dashborad.models import ZabbixHost
from dashborad.zabbix import  zb

def create_host_cache(hostid,server_obj,hostname,ip):
    try:
        zabbix_obj = ZabbixHost()
    except Exception as e:
        raise  Exception(str(e))
    else:
        zabbix_obj.server = server_obj
        zabbix_obj.zabbix_hostid = hostid
        zabbix_obj.zabbix_hostname = hostname
        zabbix_obj.zabbix_ip = ip
        zabbix_obj.save()


def create_host(server_objs,hostgroup):
    info = []
    for server_obj in server_objs:
        print server_obj
        hostname  = server_obj.hostname
        mes = {'name':hostname}
        ip = server_obj.inner_ip
        data = {"interfaces": [{"ip": ip, "useip": 1, "dns": "", "main": 1, "type": 1, "port": "10050"}], "host": hostname,  "groups": [{"groupid": hostgroup}]}
        try:
            response = Zabbix().create_hosts(data)
        except Exception as e:
            mes['mes']=str(e)

        else:
            try:
                create_host_cache(response['hostids'][0], server_obj, hostname, ip)
            except Exception as e:
                mes['mes']='操作成功但是缓存失败'
            mes['mes'] = '操作成功'
        info.append(mes)

    return  info

def get_hoststatus(server_objs):
    response = []
    for server_obj in server_objs:
        ret = {'name':server_obj.hostname,'id':server_obj.id}
        try:
            zabbix_host_obj = ZabbixHost.objects.get(server__id=server_obj.id)
        except Exception as e:
            ret['monitor'] = False
        else:
            zabbix_host_id = zabbix_host_obj.zabbix_hostid
            templates = zb.Zabbix().get_template(ids=zabbix_host_id)
            if not templates:
                ret['template_tag'] = False
            else:
                template = []
                for template in templates:
                    data = template
                    data['hostid'] = zabbix_host_obj.zabbix_hostid
                    template.append(data)
                ret['template'] = template

        response.append(ret)
        print response
    return  response

