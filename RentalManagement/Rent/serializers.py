from rest_framework import serializers
from .models import *

from decimal import Decimal

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
        fields=['id','name', 'description', 'region','city', 'sub_city',
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