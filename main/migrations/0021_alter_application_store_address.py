# Generated by Django 4.0.2 on 2022-05-09 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='store_address',
            field=models.IntegerField(default=0),
        ),
    ]