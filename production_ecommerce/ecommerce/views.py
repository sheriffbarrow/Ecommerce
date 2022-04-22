from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.views import generic
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from ecommerce.forms import ContactForm, ProductForm, Quick_ServiceForm, VendorForm, VendorImageForm, HouseImageForm, CarImageForm, RentCarForm, ProductImageForm, RentHouseForm, OrderFoodForm
from django.views.generic import TemplateView
from .import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ecommerce.models import Vendor, VendorImage, Product, ProductImage, Quick_Service, FoodImage, CarImage, HouseImage, RentCar, RentHouse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.forms import modelformset_factory
from django.conf import settings
from django.core import serializers
from account.models import UserVendor
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django import template
from django.template.loader import get_template
from django.contrib import messages
import json
from hitcount.views import HitCountDetailView
from django.db.models import Count

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def tr(request):
    return render(request, 'ecommerce/base2.html')


class Form_view(TemplateView):
    template_name = 'ecommerce/sell.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})


class HomeView(ListView):
    model = Product
    template_name = 'ecommerce/inner.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['products'] = Product.objects.all()[:10]
        context['automobile'] = RentCar.objects.all()[:5]
        context['vendors'] = Vendor.objects.all()[:10]
        context['related_products'] = Product.objects.annotate(tag_count=Count('tags')).order_by('tag_count', 'posted_date')
        context['bestseller'] = Product.objects.filter(category='')
        context['most_active'] = Product.objects.annotate(npost=Count('title')).order_by('-npost')[:5]
        context['slides'] = Vendor.objects.all().order_by('-date')[:15]
        context['cars'] = RentCar.objects.all().order_by('-pub_date')[:8]
        context['houses'] = RentHouse.objects.all().order_by('-post_date')[:8]
        return context



def account_view(request):

    if not request.user.is_authenticated:
        return redirect("account:login")

    context = {}
    if request.POST:
        form = UserVendorUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        form = UserVendorUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "contact": request.user.contact,
                "location": request.user.location,
                "profession": request.user.profession,
                "experience": request.user.experience,
            }
        )

    context['account_form'] = form

    return render(request, "account/settings.html", context)

def account_fitler(request):
    items = Product.objects.filter(vendor=request.user).order_by('-posted_date')
    context = {
        'items': items,
    }
    return render(request, 'account/account_settings.html', context)


def admin(request):
    return render(request, 'admin/base_site.html')


def slider(request):
    # change the time field in all models to posted date for uniformitty
    items = Product.objects.all()[:8]
    slides = Vendor.objects.all().order_by('-date')[:15]
    vendor = Vendor.objects.all().order_by('-date')
    cars = RentCar.objects.all().order_by('-pub_date')[:8]
    house = RentHouse.objects.all().order_by('-post_date')[:8]
    context = {
        'house': house,
        'cars': cars,
        'slides': slides,
        'items': items,
        'vendor': vendor,
    }
    return render(request, "ecommerce/temp.html", context)


def any_view(request):
    posts = Article.objects.all().order_by("-pub_date")[:5]
    return render(request, "show/temp.html", {'posts': posts})


class SellMessage(SuccessMessageMixin, CreateView):
    template_name = 'ecommerce/sell.html'
    form_class = ProductForm
    success_url = 'ecommerce:home'
    seccess_message = 'be ready to meet your buyers soon!'


class VendorView(ListView):
    model = Vendor
    template_name = 'ecommerce/index.html'
    paginate_by = 10
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.all()


@login_required(login_url='/account/login-required/')
def sell(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        imageform = forms.ProductImageForm(request.POST, request.FILES)
        img = request.FILES.getlist('productimages')
        if form.is_valid() and imageform.is_valid():
            instance = form.save(commit=False)
            instance.vendor = request.user
            instance.save()
            for f in img:
                image_instance = ProductImage(image=f, vendor=instance)
                image_instance.save()
            messages.success(request, "Product uploaded successfully and it's ready for purchase!!")
        else:
            messages.error(request, "Error!!, due to internal error or internet connectivity")
            form = VendorForm()
            imageform = ProductImageForm()
    return render(request, 'ecommerce/sell.html', {'form': ProductForm(), 'imageform': ProductImageForm()})



@login_required(login_url='/account/login-required/')
def vendor_sell(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        file_form = forms.VendorImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid() and file_form.is_valid():
            instance = form.save(commit=False)
            instance.vendor = request.user
            instance.save()
            for f in files:
                file_instance = VendorImage(file=f, vendor=instance)
                file_instance.save()
            messages.success(request, "Vendor created successfully, Good luck...!!")
        else:
            messages.error(request, "Error, due to internal or internet connectivity!!")
            form = VendorForm()
            file_form = VendorImageForm()
    return render(request, 'ecommerce/vendor_profile.html', {'form': VendorForm(), 'file_form': VendorImageForm()})


@login_required(login_url='/account/login-required/')
def vendor_sell_multiple(request):
    # number of images to be allowed
    ImageFormSet = modelformset_factory(VendorImage, fields=('file',), extra=5)
    if request.method == "POST":
        form = VendorForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            vendor = form.save(commit=False)
            vendor.vendor = request.user
            vendor.slug = slugify(vendor.title)
            vendor.save()
            for f in formset:
                try:
                    photo = VendorImage(vendor=vendor, file=f.cleaned_data['file'])
                    photo.save()
                except Exception as e:
                    break
            messages.success(request, 'succeffuly')
            return redirect('ecommerce:vendor_options')
            # this helps to not crash if the user
            # do not upload up to the max.
    else:
        form = VendorForm()
        formset = ImageFormSet(queryset=VendorImage.objects.none())
        context = {
            'form': form, 'formset': formset,
        }
    return render(request, 'ecommerce/vendor_profile.html', {'form': form, 'formset': formset})


@login_required(login_url='/account/login-required/')
def rent_car_multiple(request):
    # number of images to be allowed
    ImageFormSet = modelformset_factory(CarImage, fields=('image',), extra=5)
    if request.method == "POST":
        form = RentCarForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            vendor = form.save(commit=False)
            vendor.vendor = request.user
            vendor.save()
            for f in formset:
                try:
                    photo = CarImage(vendor=vendor, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            messages.success(request, 'succeffuly')
            return redirect('ecommerce:home')
            # this helps to not crash if the user
            # do not upload up to the max.
    else:
        form = RentCarForm()
        formset = ImageFormSet(queryset=CarImage.objects.none())
        context = {
            'form': form, 'formset': formset,
        }
    return render(request, 'ecommerce/rent_car.html', {'form': form, 'formset': formset})


@login_required(login_url='/account/login-required/')
def rent_car(request):
    if request.method == 'POST':
        form = RentCarForm(request.POST)
        carimageform = forms.CarImageForm(request.POST, request.FILES)
        img = request.FILES.getlist('carimages')
        if form.is_valid() and carimageform.is_valid():
            instance = form.save(commit=False)
            instance.vendor = request.user
            instance.save()
            for f in img:
                image_instance = CarImage(image=f, vendor=instance)
                image_instance.save()
            messages.success(
                request, "Your car has been successfully uploaded and it's ready for buyers!!")
        else:
            form = RentCarForm()
            carimageform = CarImageForm()
    return render(request, 'ecommerce/rent_car.html', {'form': RentCarForm(), 'carimageform': CarImageForm()})


@login_required(login_url='/account/login-required/')
def rent_house(request):
    if request.method == 'POST':
        form = RentHouseForm(request.POST)
        houseimageform = forms.HouseImageForm(request.POST, request.FILES)
        img = request.FILES.getlist('houseimages')
        if form.is_valid() and houseimageform.is_valid():
            instance = form.save(commit=False)
            instance.vendor = request.user
            instance.save()
            for f in img:
                image_instance = HouseImage(image=f, vendor=instance)
                image_instance.save()
            messages.success(
                request, "Your house/apartment has been successfully uploaded and it's ready for buyers!!")
        else:
            form = RentHouseForm()
            carimageform = HouseImageForm()
    return render(request, 'ecommerce/rent_house.html', {'form': RentHouseForm(), 'houseimageform': HouseImageForm()})


@login_required(login_url='/account/login-required/')
def food(request):
    if request.method == 'POST':
        form = forms.OrderFoodForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.vendor = request.user
            instance.save()
            # save to db
            return redirect('ecommerce:home')
    else:
        form = forms.OrderFoodForm()
    return render(request, 'ecommerce/food.html', {'form': form})


class Plumber(ListView):
    model = Vendor
    template_name = 'ecommerce/plumbing.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='PLUMBING')


class Electrical(ListView):
    model = Vendor
    template_name = 'ecommerce/electrical.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='ELECTRICAL')


class Cleaning(ListView):
    model = Vendor
    template_name = 'ecommerce/cleaning.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='CLEANING')


class Garden(ListView):
    model = Vendor
    template_name = 'ecommerce/garden.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='GARDEN')


class Tilin(ListView):
    model = Vendor
    template_name = 'ecommerce/tilin.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='TILING')


class Laundry(ListView):
    model = Vendor
    template_name = 'ecommerce/laundry.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='LAUNDRY')


class Carpentry(ListView):
    model = Vendor
    template_name = 'ecommerce/carpentry.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(category__iexact='CARPENTRY')


class ServiceDetail(HitCountDetailView):
    model = Vendor
    template_name = 'ecommerce/plumber-detail.html'
    context_object_name = 'detail'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ServiceDetail, self).get_context_data(**kwargs)
        context.update({
            'related_products': Vendor.objects.order_by('-hit_count_generic__hits'),
        })
        return context


class CarDetail(HitCountDetailView):
    model = RentCar
    template_name = 'ecommerce/cardetails.html'
    context_object_name = 'cardetail'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(CarDetail, self).get_context_data(**kwargs)
        context.update({
            'related_products': RentCar.objects.order_by('-hit_count_generic__hits'),
        })
        return context


class HouseDetail(HitCountDetailView):
    model = RentHouse
    template_name = 'ecommerce/housedetails.html'
    context_object_name = 'housedetail'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(HouseDetail, self).get_context_data(**kwargs)
        context.update({
            'related_products': RentHouse.objects.order_by('-hit_count_generic__hits'),
            "related_items": self.object.tags.similar_objects()[:5]
        })
        return context


def send_mail(request):
    initial_data = {
        'name': 'barrowfc',
        'service': 'de pak',
    }
    vendor = Vendor.objects.get(pk=1)
    initial_data={
                    'name': vendor.trade_name,
                    'service': vendor.category,
                    
                }
    if not request.user.is_authenticated:
        return redirect("account:login")
    
    if request.method == 'POST':
        form = ContactForm(request.POST or None, initial=initial_data)
        if form.is_valid():
            name = request.POST.get('name')
            service = request.POST.get('service')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            duration = request.POST.get('duration')
            comment = request.POST.get('comment')

            template = get_template('ecommerce/contact_form.txt')
            context = {
                'name': name,
                'service': service,
                'email': email,
                'phone': phone,
                'duration': duration,
                'comment': comment,
            }

            content = template.render(context)
            email = EmailMessage(
                "Request for Service",
                content,
                "company name" + '',
                ['farmcartt@gmail.com'],
                headers={'Reply to': email}
            )
            email.send()
            messages.success(
                request, "Request made successfuly, our correspondent will contact you shortly..!!")
        else:
            messages.error(request, "Error!! Check your internet connection and try again!!..")
            form = ContactForm()
    return render(request, 'ecommerce/contact.html', {'form': ContactForm})


class ProductDetail(HitCountDetailView):
    model = Product
    template_name = 'ecommerce/product.html'
    context_object_name = 'details'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["related_items"] = self.object.tags.similar_objects()[:5]
        context.update({
            'related_products': Product.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context

def nivoslider(request):
    return render(request, 'ecommerce/nivoslide.html')

class Shop(ListView):
    model = Product
    template_name = 'ecommerce/shop.html'
    context_object_name = 'item'
    ordering = ['-posted_date']


def electrical(request):
    return render(request, 'ecommerce/electrical.html')


def cleaning(request):
    return render(request, 'ecommerce/cleaning.html')


def garden(request):
    return render(request, 'ecommerce/garden.html')


def laundry(request):
    return render(request, 'ecommerce/laundry.html')


def tilin(request):
    return render(request, 'ecommerce/tilin.html')


def carpentry(request):
    return render(request, 'ecommerce/carpentry.html')


def vendor_profile(request):
    return render(request, 'ecommerce/vendor_profile.html')


def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'vendorprofile/profile.html', {"query": query})
    else:
        return render(request, 'vendorprofile/help.html', {})


def vendor_options(request):
    return render(request, 'ecommerce/vendor_options.html')


class Vendor_option(ListView):
    model = Quick_Service
    template_name = 'ecommerce/vendor_options.html'
    context_object_name = 'Quick_Service'

    def get_queryset(self):
        return Quick_Service.objects.all()


def accountSettings(request):
    context = {}
    return render(request, 'ecommerce/account_settings.html', context)


class Vendor_Detail(DetailView):
    model = Vendor
    template_name = 'ecommerce/'


def shop(request):
    return render(request, 'ecommerce/shop.html')


def forget(request):
    return render(request, 'ecommerce/forgot-password.html')


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "ecommerce/products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid



class ItemDetailView(DetailView):
    model = Product
    template_name = "ecommerce/product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("ecommerce:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("ecommerce:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("ecommerce:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("ecommerce:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecommerce:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("ecommerce:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("ecommerce:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecommerce:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("ecommerce:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("ecommerce:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("ecommerce:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("ecommerce:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("ecommerce:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("ecommerce:request-refund")
