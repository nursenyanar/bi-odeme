# Generated by Django 2.1.7 on 2020-08-22 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20200822_0335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sipariskayitlari',
            old_name='siparis_id',
            new_name='siparis_kayit',
        ),
    ]
