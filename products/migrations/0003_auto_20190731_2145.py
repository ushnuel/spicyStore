# Generated by Django 2.2.3 on 2019-07-31 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190509_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='location',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]