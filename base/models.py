# ------ imports -------
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator, MaxValueValidator, MinValueValidator

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)
        other_fields.setdefault('is_prime', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        other_fields.setdefault('is_verified', False)
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        email = email.lower()
        # this is done as normalization would result in 
        # 1. abc@GMAIL.COM -> abc@gmail.com
        # 2. ABC@GMAIL.COM -> ABC@gmail.com
        # Since email are unique identifiers in our app 
        # but practically both emails are exactly the same but only normalization would result in redundancy
        email = email.lower()
        name = name.strip().title()
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user

# ------ User Model -------
class NewUser(AbstractBaseUser, PermissionsMixin):

    # ------ Gender Choices -------
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    # ------ Basic Fields in User Profile -------
    email = models.EmailField(_('email address'), validators=[EmailValidator()], unique=True)
    name = models.CharField(max_length=150, blank=True, null=True, default='none')
    dateOfBirth = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(upload_to = 'images' ,default = 'images/user.png')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True, validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    address = models.CharField(max_length=200, blank=True, null=True, default='AKGEC 27th KM Milestone, Delhi - Meerut Expy, Ghaziabad, Uttar Pradesh 201009')
    
    # ------ Boolean Fields not to be accesed directly through User Profile -------
    is_seller = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_prime = models.BooleanField(default=False)

    # ------ Account Manager for Custom User Model -------
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

# ------ OTP Model -------
class OTP(models.Model):
    otp = models.IntegerField()
    otpEmail = models.EmailField()
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.otp}'