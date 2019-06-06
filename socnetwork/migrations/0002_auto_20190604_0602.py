# Generated by Django 2.2.1 on 2019-06-04 06:02

from django.conf import settings
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('socnetwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Not specified')], default='N', max_length=1, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='sub', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики'),
        ),
    ]
