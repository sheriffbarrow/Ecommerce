from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from account.models import UserVendor, Client
from django.db.models import F
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.utils import timezone
import math
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from django_resized import ResizedImageField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .utils import slugify_instance_title
from imagekit.models import ImageSpecField
from imagekit.models import ImageSpecField
import os
from pilkit.processors import ResizeToFill
from taggit.managers import TaggableManager
# Create your models here.
REGION = Choices(
                ('Ashanti', _('Ashanti')),
                ('Ahafo', _('Ahafo')),
                ('Bono', _('Bono')),
                ('Bono East', _('Bono East')),
                ('Central', _('Central')),
                ('Eastern', _('Eastern')),
                ('Greater Accra', _('Greater Accra')),
                ('Northern', _('Northern')),
                ('North East', _('North East')),
                ('Oti', _('Oti')),
                ('Savannah', _('Savannah')),
                ('UE', _('Upper East')),
                ('UW', _('Upper West')),
                ('Volta', _('Volta')),
                ('Western', _('Western')),
                ('Western North', _('Western North')),
)

VENDOR = Choices(
                ('CLEANING', _('CLEANING')),
                ('PLUMBING', _('PLUMBING')),
                ('ELECTRICAL', _('ELECTRICAL')),
                ('GARDEN', _('GARDEN')),
                ('TILING', _('TILING')),
                ('LAUNDRY', _('LAUNDRY')),
                ('CARPENTRY', _('CARPENTRY')),
)

NEG = Choices(
    ('Negotiable', _('Negotiable')),
    ('Not Negotiable', _('Not Negotiable'))
)

PRODUCT = Choices(
    ('ELECTRONICS', _('ELECTRONICS')),
    ('CLOTHING', _('CLOTHING')),
)

HOUSE = Choices(
    ('LAND', _('LAND')),
    ('APARTMENT', _('APARTMENT')),
    ('HOUSE', _('HOUSE')),
)

CAR = Choices(
    ('AUTOMOBILE', _('AUTOMOBILE')),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


Image_Folder = "media/"
#student_images = " media/student_photos"
#images = FileSystemStorage(location='/media/profile_photos')

def upload_to(instance, filename):
  now = timezone.now()
  base, extension = os.path.splitext(filename)
  extension = extension.lower()
  return f"location/{now:%Y/%m}/{instance.pk}{extension}"


class Quick_Service(models.Model):
    options = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=None)

    def __str__(self):
        return self.options


class Region(models.Model):
    region = models.CharField(max_length=255)

    def __str__(self):
        return self.region


class profile(models.Model):
    email = models.OneToOneField(UserVendor, on_delete=models.CASCADE)
    contact = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    profession = models.CharField(max_length=30)
    experience = models.CharField(max_length=30)
    verified_id = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username


class Vendor(models.Model):
    vendor = models.ForeignKey(UserVendor, on_delete=models.CASCADE)
    category = models.CharField(choices=VENDOR, default='PLUMBING', max_length=30)
    trade_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    region = models.CharField(choices=REGION, default='Greater Accra', max_length=20,)
    town = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=255)
    service_description = models.TextField(max_length=500, help_text='please be precise')
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')


    def first_image(self):
        return self.images.first()

    def __str__(self):
        return self.trade_name

    def get_absolute_url(self):
        return reverse('ecommerce:detail', kwargs={'pk': self.id})

    
    class Meta:
        ordering = ['-date']

    def slugify_instance_title(instance, save=False, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(instance.trade_name)
        qs = Vendor.objects.filter(slug=slug).exclude(id=instance.id)
        if qs.exist():
            rand_int = random.randint(300_000, 500_000)
            slug = f"{slug}-{rand_int}"
            return slugify_instance_title(instance, save=save, new_slug=slug)
        instance.slug = slug
        if save:
            instance.save()
        return instance


def post_pre_save(sender, instance, *args, **kwargs):
  print('pre_save')
  if instance.slug is None:
      slugify_instance_title(instance.rand_int + '/' + instance.trade_name, save=False)

pre_save.connect(post_pre_save, sender=Vendor)


def post_post_save(sender, instance, created, *args, **kwargs):
  print('post_save')
  if created:
    slugify_instance_title(instance, save=True)

post_save.connect(post_post_save, sender=Vendor)

class VendorImage(models.Model):
    file = models.ImageField(_('Picture'), upload_to=upload_to, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='images')
    date_posted = models.DateTimeField(auto_now_add=True, auto_now=False)
    vimage = ImageSpecField(
      source='file',
      processors=[ResizeToFill(600, 176)],
      format='JPEG',
      options={'quality': 100},
  )
    vimage2 = ImageSpecField(
      source = 'file',
      processors=[ResizeToFill(300, 363)],
      format='JPEG',
      options={'quality': 100}
  )

    class Meta:
        ordering = ['-date_posted']

@receiver(post_delete, sender=VendorImage)
def submission_delete(sender, instance, *args, **kwargs):
  instance.image.delete(False)


class Product(models.Model):
    vendor = models.ForeignKey(UserVendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    previous_price = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    percentage_discount = models.CharField(
        help_text="Do not add the '%' sign", max_length=255, default=0.00)
    contact = models.PositiveIntegerField()
    contact2 = models.PositiveIntegerField()
    posted_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    region = models.CharField(max_length=20, choices=REGION, default='Greater Accra')
    category = models.CharField(choices=PRODUCT, default='ELECTRONICS', max_length=50)
    town = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=255)
    negotiable = models.CharField(max_length=255, choices=NEG, default='Negotiable')
    description = models.TextField(max_length=500, help_text='please be precise')
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    slug = models.SlugField(max_length=255, unique=True)
    
    tags = TaggableManager()

    def first_product_image(self):
        return self.productimages.first()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ecommerce:product-details', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-posted_date']

    def slugify_instance_title(instance, save=False, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(instance.title)
        qs = Product.objects.filter(slug=slug).exclude(id=instance.id)
        if qs.exist():
            rand_int = random.randint(300_000, 500_000)
            slug = f"{slug}-{rand_int}"
            return slugify_instance_title(instance, save=save, new_slug=slug)
        instance.slug = slug
        if save:
            instance.save()
        return instance


def post_pre_save(sender, instance, *args, **kwargs):
  print('pre_save')
  if instance.slug is None:
      slugify_instance_title(instance.rand_int + '/' + instance.title, save=False)

pre_save.connect(post_pre_save, sender=Product)


def post_post_save(sender, instance, created, *args, **kwargs):
  print('post_save')
  if created:
    slugify_instance_title(instance, save=True)

post_save.connect(post_post_save, sender=Product)


class ProductImage(models.Model):
    image = models.ImageField(_('Picture'), upload_to=upload_to, blank=True, null=True)
    vendor = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productimages')
    pimage = ImageSpecField(
      source='image',
      processors=[ResizeToFill(400, 300)],
      format='JPEG',
      options={'quality': 100},
  )

@receiver(post_delete, sender=ProductImage)
def submission_delete(sender, instance, *args, **kwargs):
  instance.image.delete(False)


class RentCar(models.Model):
    vendor = models.ForeignKey(UserVendor, on_delete=models.CASCADE)
    brand = models.CharField(help_text='example: Toyota,Benz,etc.', max_length=255)
    model = models.CharField(help_text='example: corolla', max_length=255)
    model_year = models.PositiveIntegerField()
    millage = models.CharField(max_length=255, blank=True, null=True)
    manual = models.BooleanField()
    automatic = models.BooleanField()
    other = models.BooleanField()
    petrol = models.BooleanField()
    diesel = models.BooleanField()
    hybrid = models.BooleanField()
    electric = models.BooleanField()
    other = models.BooleanField()
    description = models.TextField(help_text='please be precise')
    region = models.CharField(max_length=20, choices=REGION, default='Greater Accra')
    town = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=255)
    contact = models.PositiveIntegerField()
    contact2 = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    negotiable = models.CharField(max_length=255, choices=NEG, default='Negotiable')
    pub_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def first_car_image(self):
        return self.carimages.first()

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('ecommerce:cardetail', kwargs={'pk': self.id})


class CarImage(models.Model):
    image = ResizedImageField(size=[400, 400], crop=['middle', 'center'], quality=100,
                              upload_to='car/images/', blank=True, null=True)
    vendor = models.ForeignKey(RentCar, on_delete=models.CASCADE, related_name='carimages')


class RentHouse(models.Model):
    vendor = models.ForeignKey(UserVendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    bed = models.PositiveIntegerField(help_text='Number of beds')
    bath = models.PositiveIntegerField(help_text='Number washrooms')
    description = models.TextField(max_length=50, help_text='please be precise')
    region = models.CharField(max_length=20, choices=REGION, default='Greater Accra')
    property = models.CharField(max_length=20, choices=HOUSE, default='APARTMENT')
    town = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=255)
    contact = models.PositiveIntegerField()
    contact2 = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    negotiable = models.CharField(max_length=255, choices=NEG, default='Negotiable')
    post_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def first_house_image(self):
        return self.houseimages.first()

    def __str__(self):
        return self.locality

    def get_absolute_url(self):
        return reverse('ecommerce:housedetail', kwargs={'pk': self.id})


class HouseImage(models.Model):
    image = ResizedImageField(size=[400, 400], quality=100,
                              upload_to='house/images/', blank=True, null=True)
    vendor = models.ForeignKey(RentHouse, on_delete=models.CASCADE, related_name='houseimages')


class OrderFood(models.Model):
    vendor = models.ForeignKey(UserVendor, on_delete=models.CASCADE)
    menu = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    gps_address = models.CharField(max_length=255, blank=True, null='N/A')
    contact = models.CharField(max_length=255)
    time_orderd = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.location


class FoodImage(models.Model):
    foodimage = models.ImageField(upload_to='food/images/', blank=True, null=True)
    food = models.ForeignKey(OrderFood, on_delete=models.CASCADE)
