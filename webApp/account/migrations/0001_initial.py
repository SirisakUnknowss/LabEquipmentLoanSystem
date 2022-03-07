# Generated by Django 3.2 on 2022-03-03 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(default='12345678', max_length=100, validators=[django.core.validators.MinValueValidator(8)])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('lastname', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('levelclass', models.CharField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], max_length=2, null=True)),
                ('branch', models.CharField(blank=True, max_length=100, null=True)),
                ('faculty', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('user', 'user'), ('admin', 'admin')], max_length=10, null=True)),
            ],
        ),
    ]
