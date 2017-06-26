from django.contrib import admin
from  dashborad import  models
from  django.contrib.auth.models import  Permission,ContentType

# Register your models here.

admin.site.register(models.Userprofile)
admin.site.register(models.UserGroup)
admin.site.register(models.Department)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(models.Idc)
admin.site.register(models.Server)
admin.site.register(models.Product)
admin.site.register(models.ZabbixHost)
