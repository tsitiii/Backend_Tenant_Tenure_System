from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from django.contrib import admin
from django.urls import path, include
import Rent

router=DefaultRouter()
router.register('profiles',ProfileViewSet)
router.register('property', PropertyViewSet)
router.register('notification', NotificationViewSet)
router.register('report', ReportViewSet)
router.register('rental', RentalConditionViewSet)


urlpatterns = router.urls

