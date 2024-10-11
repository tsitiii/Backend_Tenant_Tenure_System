from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site


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
            'profile_picture',
            'role',
            'password'
        ]
        extra_kwargs={
             'password': {'write_only': True}
        }
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(request=self.context.get('request'), phone=data['phone'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")


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
        # fields=['id','house_type' ,'region','city', 'sub_city',
        #         'kebele', 'unique_place','house_number','owner', 'number_of_rooms']
        fields='__all__'

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
