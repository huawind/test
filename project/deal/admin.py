from django.contrib import admin

# Register your models here.

from deal import models
admin.site.register(models.User)
admin.site.register(models.UserType)
admin.site.register(models.Goods)
admin.site.register(models.FoodTypes)
admin.site.register(models.Addgoods)
admin.site.register(models.Message)
admin.site.site_header = '管理员'
admin.site.site_title = '管理员登录'