#!/usr/bin/env python
#-*- coding:utf8 -*-
from dashborad import  models

class Ztree(object):

    def __init__(self):
        self.data = self._get_all_data()

    def _get_all_data(self):
        product_objs = models.Product.objects.all()
        return  product_objs

    def _get_second_product_obj(self,pid):
        second_product = [  objs for objs in self.data if objs.p_product is not None and objs.p_product.id ==pid]
        return  second_product


    def _get(self,isParent):
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
                if isParent:
                    tmp['children'].append({"pid": one_obj.id, "name": child.name, "id": child.id, "isParent": True})
                else:
                    tmp['children'].append({"pid":one_obj.id,"name":child.name,"id":child.id})
            ret.append(tmp)
        return ret

    def get_product(self):
        ret = self._get(isParent=False)
        return ret

    def get_zabbix(self):
        ret = self._get(isParent=True)
        return ret
