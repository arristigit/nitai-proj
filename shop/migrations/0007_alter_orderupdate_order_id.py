# Generated by Django 4.1.4 on 2023-01-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orderupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='order_id',
            field=models.ImageField(default='5000', upload_to=''),
        ),
    ]
