from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.conf import settings


user_model = settings.AUTH_USER_MODEL

class BaseUserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError('The phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)
    

class BaseUser(AbstractUser):
    objects = BaseUserManager()
    ROLE_CHOICES = (
        ('is_admin', 'Administrator'),
        ('is_tenant', 'Tenant'),
        ('is_tenure', 'Tenure'),
        ('is_witness', 'Witness'),
    ) 
    email = models.EmailField(unique=True, null=True, blank=True)
    username = None
    region=models.CharField(max_length=255, null=True, blank=False)
    city=models.CharField(max_length=100)
    sub_city=models.CharField(max_length=100)
    kebele = models.CharField(
        max_length=3,
        null=True,
        verbose_name='Kebele',
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='The kebele must be a number.'
            )
        ],
    )

    def save(self, *args, **kwargs):
        if self.kebele is None:
           self.kebele = '0'
        kebele_int = int(self.kebele)
        if 0 < kebele_int < 10:
            self.kebele = f"{kebele_int:02d}"
        elif kebele_int>9:
            self.kebele = f"{kebele_int:03d}"
        else:
            self.kebele_int = 0  
        super().save(*args, **kwargs)
    
    unique_place=models.TextField()
    house_number=models.PositiveBigIntegerField(null=True, blank=True)
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=13,
        unique=True,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^2519\d{8}$|^09\d{8}$',
                message='Please enter a valid Ethiopian phone number starting with 251 or 09 and followed by 8 digits.'
            )
        ]
    )
    kebele_ID=models.ImageField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name','password']

    

class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=255, default="Add a few words about yourself.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True)

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
    TYPE_CHOICES=(
        ("Full House", "Full House"),
        ("Service House", "Service House")
    )
    # name=models.CharField(max_length=100, null=False, db_index=True)
    # description=models.TextField()
    region=models.CharField(max_length=255, null=False)
    city=models.CharField(max_length=100)
    sub_city=models.CharField(max_length=100)
    kebele=models.CharField(max_length=255, null=True, blank= False)
    unique_place=models.TextField()
    house_number=models.PositiveBigIntegerField()
    owner=models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='property')
    house_type=models.CharField(max_length=255, choices=TYPE_CHOICES)
    number_of_rooms=models.PositiveBigIntegerField()
    def __str__(self):
        return f"{self.owner.first_name}'s Property"


class RentalCondition(models.Model):
    class Status(models.TextChoices):
        NEW_PROPERTY = "new"
        OLD_PROPERTY_NOT_BEEN_RENTED = "old_not_been_rented"
        OLD_PROPERTY_HAS_BEEN_RENTED = "old_has_been_rented"
    status=models.CharField(
        choices=Status.choices,
        max_length=100,
        verbose_name="Property condition"
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
    attachment=models.FileField(upload_to='', null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.type}- {self.name}"