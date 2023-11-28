# Generated by Django 4.2.7 on 2023-11-28 08:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.BigIntegerField(null=True, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)]),
        ),
    ]
