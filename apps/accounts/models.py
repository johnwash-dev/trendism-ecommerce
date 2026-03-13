import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        extra_fields.setdefault(
             "username",
             f"{email.split('@')[0]}_{uuid.uuid4().hex[:6]}"
        )
        
        user = self.model(email=email, **extra_fields)
        role = extra_fields.get("role", "customer")

        if role == "customer":
            user.set_unusable_password()
        elif password:
            user.set_password(password)
        else:
            raise ValueError("Password required for non-customer users")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError('Superuser must have a password')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    ROLE_CHOICES =(
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )

    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20 , choices=ROLE_CHOICES, default='customer')

    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

class Email_otp(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    attempts = models.PositiveIntegerField(default=0)
    resend_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    def __str__(self):
        return F"{self.email} - {self.otp}"
    
class SellerRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    gst_number = models.CharField(max_length=50)
    address = models.TextField()
    is_approved = models.BooleanField(default= False)
    created_at = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.user.email} - {self.shop_name}'