from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.conf import settings
from django.db.models import Q
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
        ('is_landlord', 'Landlord'),
        ('is_witness', 'Witness'),
    ) 
    email = models.EmailField(unique=True, null=True, blank=True)
    username = None
    first_name=models.CharField(max_length=255, verbose_name="your name")
    father_name=models.CharField(max_length=255, verbose_name="Father name")
    last_name=models.CharField(max_length=255, verbose_name="Grand father name")
    region=models.CharField(max_length=255, null=True, blank=False)
    city=models.CharField(max_length=100)
    sub_city=models.CharField(max_length=100)
    kebele = models.CharField(
        max_length=3,
        null=True,
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
            self.kebele = f"{kebele_int:3d}"
        else:
            self.kebele_int = 0  
        super().save(*args, **kwargs)
    
    unique_place=models.TextField()
    house_number=models.PositiveIntegerField(unique=True, null=True, blank=True)
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=13, unique=True, null=False, blank=False,
        validators=[
            RegexValidator(
                regex=r'^2519\d{8}$|^09\d{8}$',
                message='Please enter a valid Ethiopian phone number starting with 251 or 09 and followed by 8 digits.'
            )
        ]
    )

    kebele_ID=models.ImageField(upload_to='Rent/images')
    file = models.FileField('Rent/images')
    profile_picture = models.ImageField(upload_to= 'Rent/images', verbose_name= "profile picture")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True)
    created_at=models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name','password']


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=255, default="Add a few words about yourself.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='Rent/images/', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} 's profile"
    

class Notification(models.Model):
    title=models.CharField(max_length=100)
    message=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # recipient=models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='notifications')
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

    TYPE_CHOICES_PAY = (
        ("Tenant", "Tenant"),
        ("Landlord", "Landlord")
    )

    region=models.CharField(max_length=255, null=False)
    city=models.CharField(max_length=100)
    sub_city=models.CharField(max_length=100)
    kebele=models.CharField(max_length=255, null=True, blank= False)
    unique_place=models.TextField()
    house_number=models.PositiveBigIntegerField()
    owner=models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='property')
    house_type=models.CharField(max_length=255, choices=TYPE_CHOICES)
    number_of_rooms=models.PositiveIntegerField()
    class Status(models.TextChoices):
        NEW_PROPERTY = "new"
        OLD_PROPERTY_NOT_BEEN_RENTED = "old_not_been_rented"
        OLD_PROPERTY_HAS_BEEN_RENTED = "old_has_been_rented"
    status=models.CharField(
        choices=Status.choices,
        max_length=100,
        verbose_name="Property condition"
    )  
    rent_amount=models.PositiveBigIntegerField(null=False,db_index=True ,verbose_name='Rent amount in birr')
    Lease_year=models.PositiveSmallIntegerField(validators=[MinValueValidator(2)],
                                                 verbose_name= "Lease year" )
    pre_payment_birr = models.PositiveBigIntegerField(verbose_name = "pre payment paid in birr")
    pre_payment_month = models.PositiveSmallIntegerField(verbose_name = "pre  payment paid in month",
                                                          validators=[MinValueValidator(1)] )
    document = models.FileField(upload_to = 'Rent/files', verbose_name = 'ownership document')
    payment_date = models.DateTimeField(auto_now=True)
    other_bills = models.CharField(max_length=255, choices=TYPE_CHOICES_PAY)

    def __str__(self):
        return f"{self.owner.first_name}'s Property"
    

class Report(models.Model):
    total_tenants = models.PositiveIntegerField(default=0)
    total_landlords = models.PositiveIntegerField(default=0)
    total_users = models.PositiveIntegerField(default=0)
    total_admins = models.PositiveIntegerField(default=0)
    total_witnesses = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    

    @classmethod
    def update_report(cls):
     
        report, created = cls.objects.get_or_create(id=1)
        report.total_tenants = BaseUser.objects.filter(role='is_tenant').count()
        report.total_landlords = BaseUser.objects.filter(role='is_landlord').count()
        report.total_users = BaseUser.objects.exclude(role__in=['is_admin', 'is_witness']).count()
        report.total_admins = BaseUser.objects.filter(role='is_admin').count()
        report.total_witnesses = BaseUser.objects.filter(role='is_witness').count()
        report.save()
    
    def __str__(self) -> str:
        return f"{self.total_users}"
    
class ContactUs(models.Model):
    name=models.CharField(max_length=200)
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=13, unique=True, null=False, blank=False,
        validators=[
            RegexValidator(
                regex=r'^2519\d{8}$|^09\d{8}$',
                message='Please enter a valid Ethiopian phone number starting with 251 or 09 and followed by 8 digits.'
            )
        ]
    )
    message=models.TextField()

class News(models.Model):
    description=models.TextField()
    created_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='Rent/images')
    file=models.FileField(upload_to='Rent/files')
