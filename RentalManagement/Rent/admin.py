from django.contrib import admin
from .models import (
    BaseUser,
    Profile,
    Notification,
    Property,
    Report,
    ContactUs,
    News
)

class BaseUserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'first_name', 'role', 'city']
    list_filter = ['role', 'city']
    search_fields = ['first_name', 'last_name', 'phone']

admin.site.register(BaseUser, BaseUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'created_at']
    search_fields = ['user__first_name', 'user__last_name']

admin.site.register(Profile, ProfileAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'message']

admin.site.register(Notification, NotificationAdmin)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['owner', 'house_number', 'house_type', 'rent_amount']
    list_filter = ['house_type', 'status', 'owner']
    search_fields = ['unique_place', 'house_number']

admin.site.register(Property, PropertyAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ['total_tenants', 'total_landlords', 'updated_at']
    search_fields = ['total_tenants', 'total_landlords']

admin.site.register(Report, ReportAdmin)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    search_fields = ['name', 'phone']

admin.site.register(ContactUs, ContactUsAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ['description', 'created_at']
    search_fields = ['description']

admin.site.register(News, NewsAdmin)