from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class UserVendor(AbstractBaseUser):
	email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
	contact = models.IntegerField(null=True, blank=True)
	username = models.CharField(max_length=30)
	location = models.CharField(max_length=30)
	profession = models.CharField(max_length=30)
	experience = models.CharField(max_length=30)
	verified_id = models.CharField(max_length=255)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	is_active   = models.BooleanField(default=True)
	is_admin    = models.BooleanField(default=False)
	is_staff    = models.BooleanField(default=False)
	image = models.ImageField(default='profile1.png' ,upload_to='profiles/images/', null=True, blank=True)
	# notice the absence of a "Password field", that is built in.
	objects = MyAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username'] # Email & Password are required by default.

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True



class Client(AbstractBaseUser):
	email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
	contact = models.IntegerField(null=True, blank=True)
	username = models.CharField(max_length=30)
	location = models.CharField(max_length=30)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	is_active   = models.BooleanField(default=True)
	is_admin    = models.BooleanField(default=False)
	is_staff    = models.BooleanField(default=False)
	# notice the absence of a "Password field", that is built in.
	objects = MyAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username'] # Email & Password are required by default.

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
