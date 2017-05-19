#!/usr/bin/env python
# coding:utf-8
# author: xiaoyong.feng
import commands
import psutil
import subprocess
import platform
import re
import requests

class get_server_info(object):
    ## return 'opnginx1'
    def get_hostname(self):
        status,output = commands.getstatusoutput('hostname')
        return output

    ##return [{'device': 'bond0', 'ip': '10.96.52.51', 'mac': 'b0:83:fe:dc:be:d0'}, {'device': 'eth1', 'mac': 'b0:83:fe:dc:be:d0'}, {'device': 'eth0', 'mac': 'b0:83:fe:dc:be:d0'}]
    def get_device_info(self):
        ret = []
        device_white = ['eth0', 'eth1', 'eth2', 'eth3', 'bond0', 'bond1']
        device_infos = psutil.net_if_addrs()
        for interface,values in device_infos.iteritems():
            if interface in device_white:
                device_inter = {'device':interface}
                for  value in values:
                    if value.family ==2:
                        device_inter['ip'] = value.address
                    elif value.family == 17:
                        device_inter['mac'] = value.address
                ret.append(device_inter)
        return  ret

    ##return '789970kb'
    def _get_total_mem(self):
        with open('/proc/meminfo') as f:
            for line in f:
                if "MemTotal" in line:
                    memtotal =  line.split(':')[1].strip()
                    return memtotal.split(' ')[0]

    ##return "7GB" or "300MB"
    def get_mem(self):
        memtotal = int(self._get_total_mem())/1024
        if len(str(memtotal)) < 4:
            memtotal = '{0} MB'.format(round(memtotal,2))
        else:
            memtotal = '{0} GB'.format(round(memtotal/1024, 2))
        return  memtotal

    ##return {'num':3,'cpu':'Intel(R) Xeon(R) CPU E5-2403 v2 @ 1.80GHz 8'}
    def get_cpuinfo(self):
        ret = {'num': 0}
        with open('/proc/cpuinfo') as f:
            for line in f:
                if 'model name' in line:
                    ret['cpu'] = line.split(':')[1].strip()
                elif 'processor' in line:
                    ret['num']  += 1
        return  ret


    ##return "270+300"
    def get_disk(self):
        cmd = """/sbin/fdisk -l 2>>/dev/null|egrep "Disk|Platte"|egrep -v 'identifier|mapper|Disklabel'"""
        disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        partition_size = []
        for dev in disk_data.stdout.readlines():
            size = int(dev.strip().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
            partition_size.append(str(size))
        return " + ".join(partition_size)

    def get_Manufacturer(self):
        cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
        ret = {}
        manufacturer_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for man in manufacturer_data.stdout.readlines():
            if 'Manufacturer' in man:
                ret['manufacturer'] = man.split(':')[1].strip()
            elif "Product Name" in man:
                ret['server_type'] = man.split(': ')[1].strip()
            elif "Serial Number" in man:
                ret['sn'] = man.split(': ')[1].strip().replace(' ', '')
            elif 'UUID' in man:
                ret['UUID'] = man.split(':')[1].strip()
        return  ret

    def get_rel_date(self):
        cmd = """/usr/sbin/dmidecode | grep -i release"""
        data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        date = data.stdout.readline().split(': ')[1].strip()
        return re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', date)

    def get_os_version(self):
        return " ".join(platform.linux_distribution())

    def get_innerIp(self):
        device_infos = self.get_device_info()
        ret = {'inner_ip':[],'mac_address':[]}
        for device_info in device_infos:
            if device_info.has_key('ip') and device_info.has_key('mac'):
                ret['inner_ip'].append(device_info['ip'])
                ret['mac_address'].append(device_info['mac'])
        return  ret

    def send(self, data):
        url = "http://127.0.0.1:8000/server/report/"
        print data
        # r = requests.post(url, data=data)
        # print r.status_code
        # print r.content

    def run(self):
        data = {}
        data['hostname'] = self.get_hostname()
        data.update(self.get_innerIp())
        cpuinfo = self.get_cpuinfo()
        data['server_cpu'] = "{cpu} {num}".format(**cpuinfo)
        data['server_disk'] = self.get_disk()
        data['server_mem'] = self.get_mem()
        data.update(self.get_Manufacturer())
        data['manufacture_date'] = self.get_rel_date()
        data['os'] = self.get_os_version()
        if data.has_key('manufacturer'):
            if "VMware" in data['manufacturer']:
                data['vm_status'] = 0
            else:
                data['vm_status'] = 1
        else:
            raise Exception('manufacturer获取失败')
        print data
        #self.send(data)


if __name__ == "__main__":
    server_obj = get_server_info()
    server_obj.run()
