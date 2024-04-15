from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import uuid
# Create your models here.


class Formation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True , blank=True) 
    desc = models.TextField(null=True , blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    localisation = models.CharField(max_length=120 , null=True , blank=True) 
    duree = models.IntegerField(default=3)
    cout = models.IntegerField(default=1000)
    image = models.ImageField(default='default_img.jpg',upload_to='formation_images/', null=True, blank=True)
    top = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.title



class ProfileManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        # Remove the 'username' field from extra_fields
        extra_fields.pop('username', None)
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Add a default username if it doesn't exist in extra_fields
        extra_fields.setdefault('username', email)

        return self.create_user(email, password, **extra_fields)
    
    
class Profile(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True)
    numero_tel = models.CharField(max_length=12 , null=True , blank=True)
    address = models.CharField(max_length=30 , null=True , blank=True)
    niveau = models.CharField(max_length=30 , null=True , blank=True)
    
    PASSWORD_FIELD = 'password'
    
    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['numero_tel']
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Subscribe(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation , on_delete=models.SET_NULL , null=True)
    confirmed = models.BooleanField(default=False)
    
    
