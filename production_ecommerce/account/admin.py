from django.contrib.auth.admin import UserAdmin
from account.models import UserVendor,Client
from django.contrib import admin

class UserVendorAdmin(UserAdmin):
	list_display = ('email','contact','username','location','profession','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

class ClientAdmin(UserAdmin):
	list_display = ('email','contact','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('date_joined', 'last_login')

admin.site.register(UserVendor, UserVendorAdmin)
admin.site.register(Client)
