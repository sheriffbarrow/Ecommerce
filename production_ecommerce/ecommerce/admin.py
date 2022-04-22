from ecommerce.models import *
from django.contrib import admin


class Product_Admin(admin.ModelAdmin):
    list_display = ['vendor', 'title', 'price', 'previous_price', 'percentage_discount',
                    'contact', 'contact2', 'region', 'town', 'locality', 'posted_date', 'negotiable']
    prepopulated_fields = {'slug':('title',)}
    prepopulated_fields = {'tags':('category',)}


class Vendor_Admin(admin.ModelAdmin):
    list_display = ['vendor', 'category', 'trade_name',
                    'profession', 'region', 'town', 'locality', 'date']
   
    


class VendorImage_Admin(admin.ModelAdmin):
    list_display = ['file']


class RentCar_Admin(admin.ModelAdmin):
    list_display = ['vendor', 'brand', 'model', 'model_year', 'manual', 'automatic',
                    'petrol', 'diesel', 'region', 'town', 'locality', 'contact', 'contact2']


class RentHouse_Admin(admin.ModelAdmin):
    list_display = ['vendor', 'bed', 'bath', 'region', 'town', 'locality', 'description', 'contact']


class OrderFood_Admin(admin.ModelAdmin):
    list_display = ['menu', 'location', 'contact', 'time_orderd', 'is_delivered']
    list_editable = ['is_delivered']


admin.site.register(profile)
admin.site.register(Product, Product_Admin)
admin.site.register(Vendor, Vendor_Admin)
admin.site.register(VendorImage, VendorImage_Admin)
admin.site.register(Quick_Service)
admin.site.register(RentCar, RentCar_Admin)
admin.site.register(RentHouse, RentHouse_Admin)
admin.site.register(OrderFood,  OrderFood_Admin)
admin.site.register(FoodImage)
admin.site.register(HouseImage)
admin.site.register(CarImage)
admin.site.register(ProductImage)
