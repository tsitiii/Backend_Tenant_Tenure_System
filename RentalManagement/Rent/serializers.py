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
            # 'kebele',
            'unique_place',
            'house_number',
            'phone',
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
    
    
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = ['id', 'user', 'token', 'created_at', 'updated_at', 'expired_at']


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
        fields=['id','title', 'message', 'recipient','status' ]


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model=Property
        fields=['id','house_type' ,'region','city', 'sub_city',
                'kebele', 'unique_place','house_number','owner', 'number_of_rooms']

class RentalConditionSerializer(serializers.ModelSerializer):
    # payment=serializers.PositiveBigIntegerField(null=False,db_index=True, source='rent-amount' )
    class Meta:
        model=RentalCondition
        fields=['id','rent_amount','agreement_year','status']

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model=Report
        fields='__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactUs
        fields='__all__'



# class ResetPasswordEmailRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)

#     redirect_url = serializers.CharField(max_length=500, required=False)

#     class Meta:
#         fields = ['email']

#     def validate(self, attrs):
#         try:
#             email=attrs.get('email','')
#             if BaseUser.objects.filter(email=email).exists():
#                user=BaseUser.objects.get(email=email)
#                uidb64=urlsafe_base64_encode(user.id)
#                token=PasswordResetTokenGenerator().make_token(user)
#                current_site=get_current_site(request=attrs['data'].get('request')).domain
#                relativeLink=reverse('email-verify')
#                absurl='https://'+current_site + \
#                  relativeLink+"?token="+str(token)
#                email_body   ='hi'+user.username+'use the link below to verify your email.\n'
#                data={'email_body': email_body,'to_email':user.email,
#                      'email_subject':'verify your email'}
#                Util.send_email(data)
#             return attrs
#         except expression as identifier:
#             pass

#         return super().validate(attrs)
