# Generated by Django 4.2.5 on 2023-09-18 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_barcode_barcode_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(max_length=50),
        ),
    ]