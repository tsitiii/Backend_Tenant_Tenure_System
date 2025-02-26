import uuid
from .models import *
from .serializers import *
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class RegisterViewSet(ModelViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    
    access['role'] = user.role
    refresh['role'] = user.role

    return {
        'refresh': str(refresh),
        'access': str(access),
    }

@method_decorator(csrf_exempt, name='dispatch')
class LoginViewSet(viewsets.ViewSetMixin, TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)

        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(APIView):
    

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
            outstanding_token = OutstandingToken.objects.get(token=access_token)
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Token does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class WitnessViewSet(ModelViewSet):
    
    queryset=Witness.objects.all()
    serializer_class=WitnessSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class NotificationViewSet(ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer

class PropertyViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def destroy(self, request, *args, **kwargs):
        property_instance = get_object_or_404(Property, pk=kwargs['pk'])
        property_instance.delete()
        return Response({"detail": "Property deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ReportViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated
    queryset=Report.objects.all()
    serializer_class=ReportSerializer

class ContactUsViewSet(ModelViewSet):
    queryset=ContactUs.objects.all()
    serializer_class=ContactUsSerializer

class PasswordResetViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]x
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
    # permission_classes = [IsAdminUser]x
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    