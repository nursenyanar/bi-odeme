# Generated by Django 2.1.7 on 2020-08-22 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200822_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masa',
            name='kisi_say',
            field=models.IntegerField(blank=True, null=True, verbose_name='Kisi Say'),
        ),
    ]
