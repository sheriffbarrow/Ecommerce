from django.db import models

# Create your models here.
Image_Folder="media/"
#student_images = " media/student_photos"
#images = FileSystemStorage(location='/media/profile_photos')

class Teacher(models.Model):
	firstName=models.CharField(max_length=50)
	lastName=models.CharField(max_length=50)
	emailId=models.EmailField(blank=False,null=False,primary_key=True)
	contactNo=models.CharField(max_length=10)
	password=models.CharField(max_length=50)
	image = models.ImageField(upload_to=Image_Folder, null = True)

	def image_tag(self):
		  return u'<img src="/media/%s" width="100px" height="100px"/>' % self.image
	image_tag.short_description = 'Item Image'
	image_tag.allow_tags = True

	def __str__(self):
		return "%s %s %s"%(self.firstName,self.lastName,self.emailId)

	class Admin:
		pass
