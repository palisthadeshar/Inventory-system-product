# Generated by Django 4.2.5 on 2023-10-06 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_adjustment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
