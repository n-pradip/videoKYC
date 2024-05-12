from django.db import models
from utility.choices import USER_ROLES, GENDER_CHOICES
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

class UserDocument(models.Model):
    DOCUMENT_CHOICES = (
        ("nationalid","nationalid"),
        ("drivinglisence","drivinglisence"),
        ("passport","passport"),
        ("photo","nationalid"),
    )
    document_type = models.CharField(choices=DOCUMENT_CHOICES,max_length=128,null=True,blank=True)
    document = models.FileField(upload_to="user_auth_documents",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.document

class AddressModel(models.Model):
    state = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    house_no = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.state    

class InitialRegistration(models.Model):
    first_name = models.CharField(max_length=128,null=True,blank=True)
    middle_name = models.CharField(max_length=128,null=True,blank=True)
    last_name = models.CharField(max_length=128,null=True,blank=True)
    phone_no = models.CharField(max_length=10,null=True,blank=True,unique=True)
    email = models.EmailField(max_length=255,null=True,blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_otp_verified = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return self.email   

class UserManager(BaseUserManager):
    def create_user(self, email,password=None, password2=None):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self.create_user(
            email=email
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
    initial_registration_attributes = models.ForeignKey(InitialRegistration, on_delete=models.CASCADE, null=True, blank=True)
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
    is_phone_verified = models.BooleanField(default=False,null=True,blank=True)
    # is_user_verified = models.BooleanField(default=False,null=True,blank=True)
    user_document = models.ForeignKey(UserDocument, on_delete=models.CASCADE, null=True, blank=True)
    # --------------------------------------------------------------

    is_active = models.BooleanField(default=False,null=True,blank=True)  
    is_admin = models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

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
