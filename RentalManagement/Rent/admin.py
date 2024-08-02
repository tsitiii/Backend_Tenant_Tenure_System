from django.contrib import admin
from .models import BaseUser

class BaseUserAdmin(admin.ModelAdmin):
    list_display=['phone', 'first_name']
    list_filter=['phone','role','city']
    search_fields=['first_name', 'last_name', 'phone']
admin.site.register(BaseUser,BaseUserAdmin)


