from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/(\d+)/(\d+)/(\d+)/$', views.home, name="home"),
    url(r'^cart/$', views.cart, name="cart"),
    # 修改购物车
    url(r'^changecart/(\d+)/$', views.changecart, name="changecart"),
    # 下订单
    url(r'^saveorder/$', views.saveorder, name="saveorder"),
    url(r'^mine/$', views.mine, name="mine"),
    # 登陆
    url(r'^login/$', views.login, name="login"),
    # 注册
    url(r'^register/$', views.register, name="register"),
    # 验证账号是否被注册
    url(r'^checkuserid/$', views.checkuserid, name="checkuserid"),
    # 退出登陆
    url(r'^quit/$', views.quit, name="quit"),
    url(r'^messages/$',views.messages,name="messages"),
    url(r'^creat/$', views.create, name='creat'),
    url(r'^save/$', views.save, name='save'),
    url(r'^addgoods/$',views.addgoods,name='addgoods'),
]