import uuid
from .models import *
from .serializers import *
from twilio.rest import Client
from django.conf import settings
from django.utils import timezone
from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterViewSet(ModelViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    # http_method_names = ['post']
 
class LoginViewSet(viewsets.ViewSetMixin, TokenObtainPairView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class WitnessViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset=Witness.objects.all()
    serializer_class=WitnessSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class NotificationViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer

class PropertyViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset=Property.objects.all()
    serializer_class=PropertySerializer
    def destroy(self, request, *args, **kwargs):
        property=get_object_or_404(Property, pk=kwargs['pk'])
        property.delete()
        return super().destroy(request, *args, **kwargs)

class ReportViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset=Report.objects.all()
    serializer_class=ReportSerializer

class ContactUsViewSet(ModelViewSet):
    queryset=ContactUs.objects.all()
    serializer_class=ContactUsSerializer

class PasswordResetViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer
    queryset = BaseUser.objects.all()

    @action(detail=True, methods=['put']) 
    def reset_password(self, request, pk=None):
        try:
            user = BaseUser.objects.get(id=pk)
        except BaseUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['password']
            user.password = make_password(new_password)
            user.save()
            return Response({"success": "Password successfully updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class NewsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = News.objects.all()
    serializer_class = NewsSerializer