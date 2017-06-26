#!/usr/bin/env python
#-*- coding:utf8 -*-
from django.conf.urls import url ,include

from dashborad import  views
from dashborad import  user
from dashborad.user import  group,permission
from dashborad.server import  idc,product
from dashborad import server
from dashborad import zabbix
from dashborad.zabbix import template

urlpatterns = [
    url(r'^user/login/$', views.login_view),
    url(r'^user/logout/$', views.logout_view),
    url(r'^$', views.IndexView.as_view()),
    #url(r'^user/userlist/$',user.UserListView.as_view()),
    url(r'^permission/',include([
        url(r'^none/$',views.permission),
        url(r'^list/$', user.permission.PermissionView.as_view()),
        url(r'^modifycodename/$', user.permission.ModifyPermissionView.as_view()),
    ]
    ) ),
    url(r'^user/',include([
        #url(r'^userlist/$',user.UserListView.as_view()),
        url(r'^userlist/$',user.USERLISTVIEW.as_view()),
        url(r'^modifystatus/$',user.ModifyUserStatusView.as_view()),
        url(r'^modifydepartment/$',user.ModifyDepartmentView.as_view()),
        url(r'^modifyphone/$',user.ModifyPhoneView.as_view()),
        url(r'^profilelist/$',user.ProfilelistView.as_view()),

    ]
    )),
    url(r'^group/',include([
        url(r'^list/$',user.group.GroupView.as_view()),
        url(r'^add/$',user.group.GroupView.as_view()),
        url(r'^usergrouplist/$',user.group.UserGroupView.as_view()),
        url(r'^usergroupadd/$',user.group.UserGroupView.as_view()),
        url(r'^groupuserlist/$',user.group.GroupUserView.as_view()),
        url(r'^groupuserdel/$',user.group.GroupUserView.as_view()),
        url(r'^permission/$',user.group.Groupermission.as_view()),
        url(r'^permissionlist/$',user.group.GroupPermissionlist.as_view()),

    ]
    ) ),
    url(r'^server/', include([
        url(r'^idc/', include([
            url(r'^list/$',idc.ListIdcView.as_view()),
            url(r'^add/$',idc.AddIdcView.as_view()),
        ])),
        url(r'^get_sever_info_api/$',server.get_sever_info_api.as_view()),
        url(r'^list/$',server.get_server_list_view.as_view()),
        url(r'^modifystatus/$',server.ModifyStatusView.as_view()),
        url(r'^modifyproduct/$',server.ModifyProductView.as_view()),
        url(r'^productoptions/$',server.ProductOptions.as_view()),
        url(r'^product/',include([
            url(r'^list/$',product.ListProductView.as_view()),
            url(r'^add/$',product.AddProductView.as_view() ,name='product_add'),
            url(r'^list_node_info/$',product.ListNodeInfoView.as_view()),
            url(r'^modify/$',product.ModifiyView.as_view()),
            url(r'^hostlist/$',product.HostListView.as_view()),
        ])),

    ]
    )),
    url(r'^monitor/', include([
        url(r'^zabbix/',include([
            url(r'^hostrsync/$',zabbix.HostRsyncView.as_view()),
            url(r'^linktemplate/$',template.LinktemplateView.as_view()),
            url(r'^hoststatus/$',template.GetHostStatusView.as_view()),


        ])),

    ]
    )),


]