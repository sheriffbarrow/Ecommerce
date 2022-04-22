from django.contrib import admin
from vendorprofile.models import  *
# Register your models here.
class Teacher_Admin(admin.ModelAdmin):
    list_display=['emailId','contactNo','image_tag']


admin.site.register(Teacher,Teacher_Admin)
