from django.contrib.sitemaps import Sitemap
from ecommerce.models import Product




class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.posted_date