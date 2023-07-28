# Generated by Django 4.2.3 on 2023-07-20 15:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='имя пользователя')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='электронная почта')),
                ('first_name', models.CharField(max_length=30, verbose_name='имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='фамилия')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('friends', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None, verbose_name='список друзей')),
                ('image', models.ImageField(blank=True, null=True, upload_to='users/images', verbose_name='фото')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='менеджер')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='админ')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'ordering': ('id',),
            },
        ),
    ]
