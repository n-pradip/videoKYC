from django.db import models
from utility.choices import USER_ROLES, GENDER_CHOICES
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,middle_name, phone_no, role, gender, password=None, password2=None):
        """
        Creates and saves a User with the given email, phone_no, role, gender and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must provide a first name')
        if not middle_name:
            raise ValueError('Users must provide a middle name')
        if not last_name:
            raise ValueError('Users must provide a last name')
        if not role:
            raise ValueError('Users must assign a role for creating user.')
        if not gender:
            raise ValueError('Users must assign a gender for creating user.')
        
        

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name = last_name,
            phone_no=phone_no,
            role=role,
            gender=gender
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, first_name, middle_name, last_name, password=None):
        """
        Creates and saves a superuser with the given first_name, middle_name, last_name,
        email, role, phone_no.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone_no="",  #  superuser doesn't require phone_no
            role='admin', #superuser will have by default the role of admin
            password=password,
            gender='Male'
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # Custom fields ------------------------------------------------

    # --------------------------------------------------------------

    is_active = models.BooleanField(default=True,null=True,blank=True)  
    is_admin = models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserTokens(models.Model):
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    house_no = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.state
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_profile_pictures', blank=True, null=True)
    permanent_address = models.ForeignKey(AddressModel,on_delete=models.CASCADE, blank=True, null=True, related_name="user_permanent_address")
    temporary_address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, blank=True, null=True, related_name="user_temporary_address")
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=128, default='Male',null=True,blank=True)
    fathers_name = models.CharField(max_length=255, blank=True, null=True)
    mothers_name = models.CharField(max_length=255, blank=True, null=True)
    grandfathers_name = models.CharField(max_length=255, blank=True, null=True)
    spouse_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(choices=USER_ROLES, max_length=121, default='Client',null=True,blank=True)
    is_email_verified = models.BooleanField(default=False,null=True,blank=True)
    is_user_verified = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.user.email
    
class InitialRegistration(models.Model):
    first_name = models.CharField(max_length=128,null=True,blank=True)
    middle_name = models.CharField(max_length=128,null=True,blank=True)
    last_name = models.CharField(max_length=128,null=True,blank=True)
    phone_no = models.CharField(max_length=10,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email    
    

