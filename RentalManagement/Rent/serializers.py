from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
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
            'property',
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
        model=Witness
        fields=['id','first_name', 'father_name','kebele_ID','property']
    def validate(self, attrs):
        property_instance = attrs.get('property')
        witness_count = Witness.objects.filter(property=property_instance).count()
        
        if witness_count >= 3:
            raise serializers.ValidationError("This property already has 3 witnesses.")
        
        return attrs

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
    # owner = serializers.CharField(source='owner.phone')  
    # owner_phone = serializers.CharField(source='owner.phone', read_only=True)

    class Meta:
        model = Property
        fields = '__all__'

    # def create(self, validated_data):
    #     owner_phone = validated_data.pop('owner') 
    #     owner = BaseUser.objects.filter(phone=owner_phone).first()
    #     if not owner:
    #         raise serializers.ValidationError({"owner": "User with this phone number does not exist."})
    #     property_instance = Property.objects.create(owner=owner, **validated_data)
    #     return property_instance

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
