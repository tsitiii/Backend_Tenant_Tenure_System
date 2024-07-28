from django.urls import path, include
from .views import (
    ProfileViewSet,
    PropertyViewSet,
    NotificationViewSet,
    ReportViewSet,
    RentalConditionViewSet,
    RegisterViewSet,
    LoginViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profiles', ProfileViewSet)
router.register('property', PropertyViewSet)
router.register('notification', NotificationViewSet)
router.register('report', ReportViewSet)
router.register('rental', RentalConditionViewSet)
router.register('register',RegisterViewSet)
# urlpatterns=router.urls

urlpatterns = [
    path('login/', LoginViewSet.as_view({ 'post':'create'})),
    path('', include(router.urls)),
]