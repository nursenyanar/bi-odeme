# Generated by Django 2.1.7 on 2020-08-22 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20200822_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siparis',
            name='masa_no',
            field=models.IntegerField(default=1, verbose_name='masa no'),
            preserve_default=False,
        ),
    ]