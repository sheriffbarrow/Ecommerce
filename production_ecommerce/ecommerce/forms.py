from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Product, Vendor, VendorImage,ProductImage, CarImage,HouseImage, RentCar, RentHouse, OrderFood
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ClearableFileInput
User = get_user_model()
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880"


class ContactForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	phone = forms.CharField(required=True)
	duration = forms.CharField(required=True)
	comment = forms.Textarea()

class ProductForm(forms.ModelForm):

	class Meta:
		model = Product
		fields = ['title','price','previous_price','percentage_discount','contact','contact2','category','region','town','locality','negotiable','description']
		widgets = {
			'description': forms.Textarea(attrs={'rows':3, 'cols':10}),
		}

class ProductImageForm(forms.ModelForm):
	class Meta:
		model = ProductImage
		fields = ['image']

	def clean_file(self):
		file= self.cleaned_data['image']

		try:
			#validate content type
			main, sub = file.content_type.split('/')
			if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'png']):
				raise forms.ValidationError(u'Please use a JPEG or PNG image.')

			#validate file size
			if len(file) > (10000 * 1024):
				raise forms.ValidationError(u'File size may not exceed 10M.')

		except AttributeError:
			"""
			Handles case when we are updating the user profile
			and do not supply a new avatar
			"""
			pass

		return file


class VendorForm(forms.ModelForm):
	class Meta:
		model = Vendor
		fields = ['category','trade_name','profession','region','town','locality','service_description']
		widgets = {
			'service_description': forms.Textarea(attrs={'rows':3, 'cols':10}),
		}

class VendorImageForm(forms.ModelForm):


	class Meta:
		model = VendorImage
		fields = ['file']

	def clean_content(self):
		content = self.cleaned_data['file']
		content_type = content.content_type.split('/')[0]
		if content_type in settings.CONTENT_TYPES:
			if content._size > settings.MAX_UPLOAD_SIZE:
				raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
		else:
			raise forms.ValidationError(_('File type is not supported'))
		return content

class RentCarForm(forms.ModelForm):
	 class Meta:
		 model = RentCar
		 fields = ['brand','model','model_year','millage','manual','automatic','other','petrol',
					'diesel','hybrid','electric','other','description','region','town','locality','contact','contact2','price','negotiable']
		 widgets = {
			 'description': forms.Textarea(attrs={'rows':3, 'cols':10}),

		 }

class CarImageForm(forms.ModelForm):
	class Meta:
		model = CarImage
		fields = ['image']


class RentHouseForm(forms.ModelForm):
	class Meta:
		model = RentHouse
		fields = ['title','bed','bath','description','property','region','town','locality','contact','contact2','price','negotiable']
		widgets = {
			'description': forms.Textarea(attrs={'rows':3, 'cols':10}),
		}

class HouseImageForm(forms.ModelForm):
	class Meta:
		model = HouseImage
		fields = ['image']

class OrderFoodForm(forms.ModelForm):
	class Meta:
		model = OrderFood
		fields = ['menu', 'location','gps_address','contact']


class Quick_ServiceForm(forms.Form):
	client_name = forms.CharField(required=True)
	client_email = forms.EmailField(required=True)
	number = forms.IntegerField(required=True)
	client_comment = forms.CharField(required=True)
