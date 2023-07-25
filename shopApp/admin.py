from django.contrib import admin
# from .models import catagory
from .models import *
# Register your models here.
# class Admin(admin.ModelAdmin):
#     list_display=('name','description','status','created_at')
admin.site.register(catagory)
admin.site.register(products)