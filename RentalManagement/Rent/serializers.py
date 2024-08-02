from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    class Meta:
        model=BaseUser
        fields = [
            'id',
            'first_name',
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

class WitnessSerializer(serializers.ModelSerializer):
    class Meta:
        model=BaseUser
        fields=['first_name', 'last_name','kebele_ID', 'role']


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
        fields=['id','type', 'name', 'description', 'attachment']