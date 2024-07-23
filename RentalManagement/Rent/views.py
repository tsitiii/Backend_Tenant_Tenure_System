from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from django.http import FileResponse
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class NotificationViewSet(ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer

class PropertyViewSet(ModelViewSet):
    queryset=Property.objects.all()
    serializer_class=PropertySerializer
    def destroy(self, request, *args, **kwargs):
        property=get_object_or_404(Property, pk=kwargs['pk'])
        property.delete()
        return super().destroy(request, *args, **kwargs)

class RentalConditionViewSet(ModelViewSet):
    queryset=RentalCondition.objects.all()
    serializer_class=RentalConditionSerializer

class ReportViewSet(CreateModelMixin,GenericViewSet):
    queryset=Report.objects.all()
    serializer_class=ReportSerializer
