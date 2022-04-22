from django.test import TestCase

# Create your tests here.
def registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        location= request.POST['location']
        profession = request.POST['profession']
        experience = request.POST['experience']
        verified_id = request.POST['verified_id']
        date_of_birth = request.POST['date_of_birth']
        image = request.POST['image']

        user = User.objects.create_user(email=email, location=location,profession=profession,experience=experience,verified_id=verified_id, date_of_birth=date_of_birth,image=image)
        user.save();
        print('user created')
        return redirect('ecommerce:HomeView')
    else:
        return render(request, 'ecommerce/register.htmls')
