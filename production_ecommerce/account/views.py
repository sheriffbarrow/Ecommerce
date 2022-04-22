from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, UserVendorAuthenticationForm, UserVendorUpdateForm, RegistrationclientForm
from django.contrib.auth import get_user_model
from ecommerce.models import Product, Vendor, RentCar, RentHouse, OrderFood
from ecommerce.forms import ProductForm, VendorForm, RentCarForm, RentHouseForm, OrderFoodForm
from django.contrib import messages
from .import forms
from account.models import UserVendor
User = get_user_model()
# Create your views here.


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('ecommerce:home')
    else:
        context = {}
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                messages.success(request, "Account created successfully, login now!!..")
                #messages.success(request, f'Your order has been placed successfully our correspondent will get contact you shortly')
                # login(request,account)
                return redirect('account:login')
            else:
                messages.warning(
                    request, "Error, unable to create account, please correct the errors below!!")
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, 'ecommerce/registervendor.html', context)


def registration_client_view(request):
    context = {}
    if request.POST:
        form = RegistrationclientForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            # login(request,account)
            return redirect('account:login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationclientForm()
        context['registration_form'] = form
    return render(request, 'ecommerce/client.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("ecommerce:home")

    if request.POST:
        form = UserVendorAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("ecommerce:home")

    else:
        form = UserVendorAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "ecommerce/login.html", context)


def login_view_required(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("ecommerce:home")

    if request.POST:
        form = UserVendorAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("ecommerce:home")

    else:
        form = UserVendorAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "ecommerce/login_required.html", context)


def account_view(request):
    initial_data={
                "email": request.user.email,
                "contact": request.user.contact,
                "username": request.user.username,
                "location": request.user.location,
                "profession": request.user.profession,
                "experience": request.user.experience,
            }
        
    if not request.user.is_authenticated:
        return redirect("account:login")

    context = {}
    if request.POST:
        form = UserVendorUpdateForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        
        form = UserVendorUpdateForm(initial = initial_data)
            

    context['account_form'] = form

    return render(request, "account/settings.html", context)


def account_fitler(request):
    items = Product.objects.filter(vendor=request.user).order_by('-posted_date')
    context = {
        'items': items,
    }
    return render(request, 'account/account_settings.html', context)


def accountSettings(request):
    customer = request.user

    context = {'customer': customer,
               }
    return render(request, 'account/account_settings.html', context)
