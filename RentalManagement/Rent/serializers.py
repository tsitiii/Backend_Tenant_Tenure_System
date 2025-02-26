from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    class Meta:
        model=BaseUser
        fields = [
            'id',
            'first_name',
            'father_name',
            'last_name',
            'region',
            'city',
            'sub_city',
            'kebele',
            'unique_place',
            'house_number',
            'phone',
            'role',
            'kebele_ID',
            'file',
            'profile_picture',
            'password'
        ]
        extra_kwargs={
             'password': {'write_only': True}
        }
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(request=self.context.get('request'), phone=data['phone'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError(_("Invalid credentials."))
        if not user.is_active:
            raise serializers.ValidationError(_("User account is not active."))
        data['user'] = user
        return data

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
       model =  BaseUser
       fields = ['password']

class WitnessSerializer(serializers.ModelSerializer):
    class Meta:
        model=BaseUser
        fields=['first_name', 'father_name','kebele_ID', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    # picture = serializers.ImageField(null=True, blank=True, source='profile_picture')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'profile_picture']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['id','title', 'message','status' ]

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields='__all__'
    
    def validate_owner(self, value):
        
        if not BaseUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Invalid owner ID.")
        return value

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model=Report
        fields='__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactUs
        fields='__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
