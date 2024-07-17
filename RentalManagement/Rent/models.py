from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class BaseUser(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=150, unique=True)
    region=models.CharField(max_length=255, null=True, blank=False)
    city=models.CharField(max_length=100)
    sub_city=models.CharField(max_length=100)
    kebele=models.CharField(max_length=255, null=True, blank= False)
    unique_place=models.TextField()
    house_number=models.PositiveBigIntegerField()
    phone=models.PositiveIntegerField()
    is_admin=models.BooleanField(default=False)
    is_witness=models.BooleanField(default=False)
    User = get_user_model()

class Tenant(BaseUser):
    pass

class Tenure(BaseUser):
    pass


class Profile(models.Model):
     user=models.OneToOneField(BaseUser,on_delete=models.CASCADE, related_name='profile')
     bio=models.TextField(blank=True, max_length=255, default="Add a few words about yourself.")
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)
     picture=models.ImageField(upload_to='/', null=True, blank=True)
     
     def __str__(self) -> str:
         return f"{self.user.username} 's profile"
     
class Notification(models.Model):
    title=models.CharField(max_length=100)
    message=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    recipient=models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='notifications')
    class Status(models.TextChoices):
        DRAFT='draft' 
        SENT='sent'
        READ='read'
    status=models.CharField(
        max_length=140,
        choices= Status.choices,
        default=Status.DRAFT
    )
    def __str__(self) -> str:
        return f"{self.title} - {self.get_status_display()}"    

class Property(models.Model):
    name=models.CharField(max_length=100, null=False, db_index=True)
    description=models.TextField()
    region=models.CharField(max_length=255, null=False)
    city=models.CharField(max_length=100)
    sub_city=models.CharField(max_length=100)
    kebele=models.CharField(max_length=255, null=True, blank= False)
    unique_place=models.TextField()
    house_number=models.PositiveBigIntegerField()
    owner=models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    number_of_rooms=models.PositiveBigIntegerField()

class RentalCondition(models.Model):
    class Status(models.TextChoices):
        PROPERTY_NEW = "new"
        PROPERTY_OLD_NOT_RENTED = "old_not_been_rented"
        PROPERTY_OLD_RENTED = "old_has_been_rented"
    status=models.CharField(
        choices=Status.choices
    )  
    rent_amount=models.PositiveBigIntegerField(null=False,db_index=True )
    agreement_year=models.PositiveSmallIntegerField(
          validators=[MinValueValidator(2)]
    )
    
    def __str__(self) -> str:
        return f"Rented: {self.rent_amount},Birr for {self.agreement_year} "
    

class Report(models.Model):
    type=models.CharField(max_length=100)
    name=models.CharField(blank=False, null=False, max_length=100)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    attachment=models.FileField(upload_to='/', null=True, blank=True)
    