# Generated by Django 3.2.5 on 2021-09-21 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_product_isoutofstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='isAvailable',
            field=models.BooleanField(default=True),
        ),
    ]
