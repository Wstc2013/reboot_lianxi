#-*-coding:utf8-*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    class Meta:
        db_table = 'department'
        permissions = (
            ("view_userlist", "can view userlist"),
            ("view_grouplist", "can view grouplist"),
            ("view_groupuser", "can view group user"),
            ("add_groupuser", "can add group user"),
            ("del_groupuser", "can del group user"),
            ("view_usergroup", "can view user group"),
            ("add_usergroup", "can add user group"),
            ("change_groupermission", "can change group permission"),




        )


class Userprofile(models.Model):
    user = models.OneToOneField(User)
    department = models.ForeignKey('Department')
    phone = models.CharField(max_length=11, null=True)
    title = models.CharField(max_length=32, null=True)
    name = models.CharField(u'中文名',max_length=32, null=True)
    email = models.EmailField(max_length=32)
    class Meta:
        db_table = 'userprofile'
        default_related_name = 'userprofile'


class UserGroup(models.Model):
    name = models.CharField(max_length=32)
    user = models.ManyToManyField('Userprofile')




class Idc(models.Model):
    name = models.CharField("idc 字母简称",max_length=10,unique=True)
    idc_name = models.CharField("idc 中文名",max_length=100)
    idc_address = models.CharField("机房的具体地址",max_length=255)
    idc_user = models.ForeignKey('Userprofile')

    class Meta:
        db_table = 'idc'
        permissions = (
            ("view_idc", "can view idc"),
        )

class Product(models.Model):
    name = models.CharField("业务线名称",max_length=32)
    p_product = models.ForeignKey("self",null=True,verbose_name="上级业务线")
    module_letter = models.CharField("字母简称",max_length=10)
    op_interface = models.CharField("运维负责人: username1,username2",max_length=255)
    dev_interface = models.CharField("业务负责人: username1,username2", max_length=255)

    def __str__(self):
        return "{}".format(self.module_letter)

    class Meta:
        db_table = "product"
        permissions = (
            ("view_product", "访问业务线"),
        )

class Server(models.Model):
    supplier        = models.IntegerField(null=True)
    manufacturers   = models.CharField(max_length=50, null=True)
    manufacture_date= models.DateField(null=True)
    server_type     = models.CharField(max_length=20, null=True)
    sn              = models.CharField(max_length=60, db_index=True, null=True)
    idc             = models.ForeignKey(Idc, null=True)
    os              = models.CharField(max_length=50, null=True)
    hostname        = models.CharField(max_length=50, db_index=True, null=True)
    inner_ip        = models.CharField(max_length=32, null=True, unique=True)
    mac_address     = models.CharField(max_length=50, null=True)
    ip_info         = models.CharField(max_length=255, null=True)
    server_cpu      = models.CharField(max_length=250, null=True)
    server_disk     = models.CharField(max_length=100, null=True)
    server_mem      = models.CharField(max_length=100, null=True)
    status          = models.CharField(max_length=100,db_index=True, null=True)
    remark          = models.TextField(null=True)
    #service_id      = models.IntegerField(db_index=True, null=True)
    server_business  = models.ForeignKey(Product,null=True,related_name='server_business')
    server_product = models.ForeignKey(Product, null=True,related_name='server_product')
    create_time     = models.DateTimeField(null=True,auto_now_add=True)
    check_update_time = models.DateTimeField(null=True,auto_now=True)
    vm_status       = models.IntegerField(db_index=True, null=True)
    uuid            = models.CharField(max_length=100, db_index=True,null=True)


    def __str__(self):
        return "{} {}".format(self.hostname, self.inner_ip)

    class Meta:
        db_table = "server"
        permissions = (
            ("view_server", "访问服务器信息"),
        )

class Status(models.Model):
    name = models.CharField(max_length=32)



