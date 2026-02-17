from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validate_phone_number 
# --------------------------------------------------------------------------------------------
class UserType(models.IntegerChoices) :
    CUSTOMER = 1, 'Customer'
    ADMIN = 2, 'Admin'
    SUPER_ADMIN = 3, 'Super Admin'
# --------------------------------------------------------------------------------------------
class UserManager(BaseUserManager) :
    '''
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    '''

    def create_user(self, email, password=None,**extra_fields):
        '''
         Creates and saves a User with the given email,  and password.
        '''
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    # ------------------------
    def create_superuser(self, email, password=None,**extra_fields):
        """
        Creates and saves a superuser with the given email,  and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("type", UserType.SUPER_ADMIN.value)
        return self.create_user(email, password, **extra_fields)
    
# --------------------------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin) :

    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True)
    type = models.PositiveSmallIntegerField(choices=UserType.choices, default=UserType.CUSTOMER.value)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
# --------------------------------------------------------------------------------------------
class Profile(models.Model) :
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], blank=True, null=True)
    image = models.ImageField(upload_to='profiles/',default='profiles/default.jpg', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True) 
    updated_date = models.DateTimeField(auto_now=True)
    descriptions = models.TextField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.email
# --------------------------------------------------------------------------------------------
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Signal creation: When creating a user, a profile is automatically created.
    '''
    # if created and instance.type == UserType.CUSTOMER.value:
    #     Profile.objects.create(user=instance)
    if created:
        Profile.objects.create(user=instance)
# --------------------------------------------------------------------------------------------
