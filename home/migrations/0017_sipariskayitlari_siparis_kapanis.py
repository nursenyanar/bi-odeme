# Generated by Django 2.1.7 on 2020-08-25 01:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20200823_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='sipariskayitlari',
            name='siparis_kapanis',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Kapanış saati'),
            preserve_default=False,
        ),
    ]