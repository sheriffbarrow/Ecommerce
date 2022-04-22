from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import UserVendor,Client


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput, max_length=254, help_text='Required. Add a valid email address.')
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='password must not be entirely numeric and must contain at least 8 characters')
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = UserVendor
		fields = ('email', 'username','contact','location','profession','experience','verified_id','image', 'password1', 'password2', )
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'input'}),
			'username': forms.TextInput(attrs={'class': 'input'}),
		}

class RegistrationclientForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput, max_length=254, help_text='Required. Add a valid email address.')
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Client
		fields = ('email','contact','username','password1', 'password2', )
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'input'}),
			'username': forms.TextInput(attrs={'class': 'input'}),
		}

class UserVendorAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)


	class Meta:
		model = UserVendor
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")



class UserVendorUpdateForm(forms.ModelForm):

	class Meta:
		model = UserVendor
		fields = ('email', 'username','contact','location','profession','experience')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = UserVendor.objects.exclude(pk=self.instance.pk).get(email=email)
			except UserVendor.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = UserVendor.objects.exclude(pk=self.instance.pk).get(username=username)
			except UserVendor.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.' % username)
