# Generated by Django 2.1.5 on 2021-12-13 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_remove_vendor_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='slug',
        ),
    ]
