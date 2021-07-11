from django.contrib import admin
from .models import visitor, access
# Register your models here.

# 顯示資料庫
admin.site.register(visitor)
admin.site.register(access)